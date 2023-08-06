import os

from functools import partial
from typing import List, Optional

from ..core import gpg
from ..core.archive import (
    check_package,
    extract,
    unpack_from_stream,
    DATA_ARCHIVE,
    DATA_FILE_ENCRYPTED,
    CHECKSUM_FILE,
    extract_with_progress,
)
from ..core.crypt import (
    check_password_matches_any_key,
    decrypt as core_decrypt,
    enforce_passphrase,
    retrieve_refresh_and_validate_keys,
    fingerprint2keyid,
    verify_metadata_signature,
)
from ..core.filesystem import (
    DeleteDirOnError,
    get_compression_stats,
    get_total_size,
    to_human_readable_size,
    unique_filename,
    check_space,
)
from ..core.checksum import verify_checksums, read_checksum_file
from ..core.secret import Secret
from ..utils.log import create_logger, log_runtime_info, log_timing
from ..utils.progress import ProgressInterface, subprogress
from ..utils.config import Config


logger = create_logger(__name__)


@log_timing(logger)
@log_runtime_info(logger)
def decrypt(
    files: List[str],
    *,
    passphrase: Optional[Secret[str]] = None,
    output_dir: str,
    config: Config,
    decrypt_only: bool = False,
    dry_run: bool = False,
    progress: Optional[ProgressInterface] = None,
) -> None:
    """Main function of the decrypt workflow. Decrypts and decompresses the
    input archive files."""

    logger.info(
        "File(s) to decrypt: [%s], output_dir: %s%s",
        ", ".join(files),
        output_dir,
        " (dry_run)" if dry_run else "",
    )

    with logger.log_task("Input data check"):
        for archive_path in files:
            check_package(archive_path)

    check_space(get_total_size(files), output_dir, force=False)

    if dry_run:
        logger.info("Dry run completed successfully.")
        return

    for archive_file in files:
        # Reset progress for each tar file
        if progress is not None:
            progress.update(0.0)
        decrypt_archive(
            archive_file,
            passphrase=passphrase,
            output_dir=output_dir,
            config=config,
            decrypt_only=decrypt_only,
            progress=progress,
        )


def decrypt_archive(
    archive_file: str,
    passphrase: Optional[Secret[str]],
    output_dir: str,
    config: Config,
    decrypt_only: bool = False,
    progress: Optional[ProgressInterface] = None,
) -> None:
    """Decrypts and decompresses the input archive_file."""

    logger.info("Processing file %s", archive_file)
    # To avoid overwriting files, each archive is unpacked in a directory
    # that has the same name as the archive file minus its extension.
    out_dir = unique_filename(
        os.path.splitext(os.path.join(output_dir, os.path.basename(archive_file)))[0]
    )

    with DeleteDirOnError(out_dir):
        with logger.log_task("Verifying signatures..."):
            verify_metadata_signature(
                tar_file=archive_file,
                gpg_store=config.gpg_store,
                signee_fingerprint=None,
                key_authority_fingerprint=config.key_authority_fingerprint,
                keyserver_url=config.keyserver_url,
                validate_key_origin=False,
            )

        with logger.log_task("Verifying encryption keys..."), extract(
            archive_file, DATA_FILE_ENCRYPTED
        ) as f_data:
            keys = list(
                retrieve_refresh_and_validate_keys(
                    key_search_terms=gpg.extract_key_id(f_data),
                    gpg_store=config.gpg_store,
                    key_authority_fingerprint=config.key_authority_fingerprint,
                    keyserver_url=config.keyserver_url,
                    allow_key_download=config.allow_gpg_key_autodownload,
                )
            )
            logger.info(
                "Data encrypted for: %s",
                ", ".join(f"{key.uids[0]} ({key.fingerprint})" for key in keys),
            )
            check_password_matches_any_key(
                password=enforce_passphrase(passphrase),
                keys=keys,
                gpg_store=config.gpg_store,
            )

        unpacked_files: List[str] = []
        with logger.log_task("Decrypting data..."), subprogress(
            progress, step_completion_increase=0.95
        ) as scaled_progress, extract_with_progress(
            archive_file, scaled_progress, DATA_FILE_ENCRYPTED
        ) as f_data:
            os.makedirs(out_dir, exist_ok=True)
            if decrypt_only:
                sender_fprs = core_decrypt(
                    source=f_data,
                    output=os.path.join(out_dir, DATA_ARCHIVE),
                    gpg_store=config.gpg_store,
                    passphrase=passphrase,
                )
            else:
                sender_fprs = core_decrypt(
                    source=f_data,
                    output=partial(
                        unpack_from_stream, dest=out_dir, content=unpacked_files
                    ),
                    gpg_store=config.gpg_store,
                    passphrase=passphrase,
                )
            sender_sig_keys = retrieve_refresh_and_validate_keys(
                key_search_terms=map(fingerprint2keyid, sender_fprs),
                gpg_store=config.gpg_store,
                key_authority_fingerprint=config.key_authority_fingerprint,
                keyserver_url=config.keyserver_url,
                allow_key_download=config.allow_gpg_key_autodownload,
            )
            logger.info(
                "Data signed by: %s",
                ", ".join(
                    f"{key.uids[0]} ({key.fingerprint})" for key in sender_sig_keys
                ),
            )

        with subprogress(progress, step_completion_increase=0.05) as scaled_progress:
            if decrypt_only:
                decryption_stats = "size: " + to_human_readable_size(
                    os.path.getsize(archive_file)
                )
            else:
                with logger.log_task(
                    "Checksum verification of uncompressed data..."
                ), open(os.path.join(out_dir, CHECKSUM_FILE), "rb") as fout:
                    # Path separator replacement is a fail-safe if paths are not POSIX.
                    verify_checksums(
                        [
                            (c, os.path.join(out_dir, p.replace("\\", os.path.sep)))
                            for c, p in read_checksum_file(fout)
                        ],
                        # `max_workers` accepts only None and positive integers. Make
                        # sure that zero and negative values are converted into None.
                        max_workers=config.max_cpu if config.max_cpu > 0 else None,
                    )
                log_files(unpacked_files)
                decryption_stats = get_compression_stats(
                    os.path.getsize(archive_file),
                    get_total_size(os.path.join(out_dir, f) for f in unpacked_files),
                    compression=False,
                )
            if scaled_progress is not None:
                scaled_progress.update(1.0)
            logger.info(
                "Completed data decryption: %s (%s)", archive_file, decryption_stats
            )


def log_files(files: List[str]) -> None:
    max_files_to_list = 5
    d_n = len(files) - max_files_to_list
    logger.info(
        "Extracted files: [%s] %s",
        ", ".join(files[:max_files_to_list]),
        ((f"and {d_n} more files - not listing them all.") if d_n > 0 else ""),
    )
