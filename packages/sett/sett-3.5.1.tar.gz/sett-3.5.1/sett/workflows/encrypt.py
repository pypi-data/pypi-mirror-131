from datetime import datetime
import io
import json
import os
from functools import partial
from pathlib import Path
from typing import List, Optional, Callable, Tuple, Iterable, Any, TypeVar
from zipfile import ZipFile, ZipInfo, ZIP_STORED

from ..core import gpg
from ..core.archive import (
    write_tar,
    ArchiveInMemoryFile,
    ArchiveFile,
    ArchiveFileBase,
    METADATA_FILE,
    METADATA_FILE_SIG,
    DATA_FILE_ENCRYPTED,
    CHECKSUM_FILE,
    CONTENT_FOLDER,
)
from ..core.filesystem import (
    delete_file_on_error,
    get_compression_stats,
    get_total_size,
    search_files_recursively,
    check_file_read_permission,
    check_space,
)
from ..core.crypt import (
    enforce_passphrase,
    retrieve_refresh_and_validate_keys,
    encrypt_and_sign,
    detach_sign_file,
    check_password,
    search_priv_key,
)
from ..core.checksum import generate_checksums_file_content, compute_checksum_on_write
from ..core.error import UserError
from ..core.metadata import MetaData, alnum_str, Purpose, HexStr1024, HexStr256
from ..core.secret import Secret
from ..core.portal_api import PortalApi
from ..utils.progress import ProgressInterface, subprogress, progress_file_iter
from ..utils.config import Config
from ..utils.log import create_logger, log_runtime_info, log_timing

DATE_FMT_FILENAME = "%Y%m%dT%H%M%S"
logger = create_logger(__name__)
output_name_str = alnum_str(min_length=1, max_length=50, allow_dots=True)


def path_str(directory: bool = False, writable: bool = False) -> Callable[[str], str]:
    """Generate a 'type definition' function that will check that a string is
    a valid path (file or directory).

    :param directory: if True, the path must be a directory.
    :param writable: if True, the user must have write access to the path.
    :returns: type check function.
    :raises ValueError:
    """

    def _path_str(path_to_check: str) -> str:
        path = Path(path_to_check)
        if not path.exists():
            raise ValueError(f"Invalid path: '{path_to_check}'. Path does not exist.")
        if directory and not path.is_dir():
            raise ValueError(
                f"Invalid path: '{path_to_check}'. Path is not a directory."
            )
        if writable and not os.access(path.as_posix(), os.W_OK):
            raise ValueError(f"Invalid path: '{path_to_check}'. Path is not writable.")
        return path_to_check

    return _path_str


output_path_str = path_str(directory=True, writable=True)


def check_integer_in_range(min_value: int, max_value: int) -> Callable[[Any], None]:
    """Generate a function that will check that its input value is an integer,
    and that this integer is in the range [min_value:max_value].
    """

    def _integer_in_range(value_to_check: Any) -> None:
        try:
            value_to_check = int(value_to_check)
        except ValueError as e:
            raise ValueError("Value must be an integer") from e

        if value_to_check < min_value or value_to_check > max_value:
            raise ValueError(f"Value must be in the range: [{min_value}-{max_value}]")

    return _integer_in_range


def check_paths_on_posix(paths: Iterable[str]) -> None:
    """Check paths for windows-style separators.

    If the machine is POSIX, verify that the specified paths do not contain
    any windows-style separators.
    """

    for path in paths:
        if os.path.sep == "/" and "\\" in path:
            raise UserError(
                "On POSIX systems (this machine), backslashes are NOT allowed "
                f"as path separators. Offending value is [{path}]."
            )


check_compression_level = check_integer_in_range(min_value=0, max_value=9)


@log_timing(logger)
@log_runtime_info(logger)
def encrypt(  # pylint: disable=too-many-statements
    files: List[str],
    *,
    config: Config,
    recipient: List[str],
    dtr_id: Optional[int] = None,
    sender: Optional[str] = None,
    passphrase: Optional[Secret[str]] = None,
    output: Optional[str] = None,
    output_suffix: Optional[str] = None,
    dry_run: bool = False,
    verify_dtr: bool = True,
    force: bool = False,
    compression_level: Optional[int] = None,
    purpose: Optional[Purpose] = None,
    progress: Optional[ProgressInterface] = None,
) -> Optional[str]:
    """Compress and encrypt files and/or directories.

    Main function of the encryption workflow. It compresses the input files
    into a single archive file, which is then encrypted for the specified
    recipient and signed by the specified sender.
    Finally, the encrypted data is bundled with a metadata file in a single
    .zip archive.
    The function returns the file name of the created package.
    """

    # Retrive non-specified, optional argument values from config.
    if sender is None:
        sender = config.default_sender or config.gpg_store.default_key()
        if sender is None:
            raise UserError("Sender not specified with no default sender.")
    if compression_level is None:
        compression_level = config.compression_level
    check_arg_value(
        arg_value=compression_level,
        arg_name="compression level",
        arg_type_checker=check_compression_level,
    )

    if not files:
        raise UserError("Empty file list")

    files_to_encrypt = list(search_files_recursively(files))

    with logger.log_task("Input data check"):
        if not files_to_encrypt:
            raise UserError(
                "No input files found. Did you try encrypting an empty directory?"
            )
        check_file_read_permission(files_to_encrypt)
        # Retrieve the lowest common directory of all input files/directories.
        root_dir = os.path.commonpath(
            [Path(x).absolute().parent.as_posix() for x in files]
        )
        if dtr_id is None and verify_dtr:
            raise UserError("DTR (Data Transfer Request) ID is missing.")
        if output_suffix:
            check_arg_value(output_suffix, "output suffix", output_name_str)

    with logger.log_task("Retrieve sender and recipient GnuPG keys"):
        # Retrieve the sender's public and private keys, as well as the
        # recipient's public key. Here is what these keys are needed for:
        #  - sender private key: needed to sign the encrypted data.
        #  - sender public key : will be checked to make sure it is signed by
        #       the DCC. Only private keys with a matching public key that is
        #       signed by the DCC will be allowed to be used.
        #  - recipient public key: needed to encrypt the data.
        #
        # The sender/recipient information can be either an email, a keyID or
        # a full fingerprint.
        sender_pub_key, *recipients_pub_key = retrieve_refresh_and_validate_keys(
            key_search_terms=(sender, *recipient),
            gpg_store=config.gpg_store,
            key_authority_fingerprint=config.key_authority_fingerprint,
            keyserver_url=config.keyserver_url,
            validate_key_origin=False,
            allow_key_download=config.allow_gpg_key_autodownload,
        )

        # Verify a private key matching the user's public key exists. The key
        # itself is not needed because it shares the fingerprint with the
        # public key.
        search_priv_key(sender_pub_key.fingerprint, config.gpg_store)

        logger.info(
            "Sender: %s. Recipients: %s",
            f"{sender_pub_key.uids[0]} ({sender_pub_key.fingerprint})",
            ", ".join(
                f"{key.uids[0]} ({key.fingerprint})" for key in recipients_pub_key
            ),
        )

    project_code = determine_project_code(
        dtr_id,
        purpose,
        config.portal_api if not config.offline and verify_dtr else None,
        sender_pub_key,
        recipients_pub_key,
    )

    timestamp = datetime.now().astimezone()
    # The default value for the output name is based on date and time
    # when the script is being run.
    # Example output name is "20191011T145012".
    output_name = generate_output_archive_name(
        output,
        default="_".join(
            filter(
                None,
                [
                    project_code,
                    timestamp.strftime(DATE_FMT_FILENAME),
                    output_suffix or config.package_name_suffix,
                ],
            )
        ),
    )
    total_input_file_size = get_total_size(files_to_encrypt)
    check_space(total_input_file_size, os.path.dirname(output_name), force=force)

    # Create a list of file paths (of the files that are being packaged) as they
    # will appear in the output archive file.
    archive_paths = [
        os.path.join(CONTENT_FOLDER, os.path.relpath(f, start=root_dir))
        for f in files_to_encrypt
    ]

    check_paths_on_posix(archive_paths)

    if dry_run:
        logger.info("Dry run completed successfully")
        return None

    # If the user asked to sign the data, check that the GPG key password
    # is correct.
    if config.sign_encrypted_data:
        check_password(
            password=enforce_passphrase(passphrase),
            key_fingerprint=sender_pub_key.fingerprint,
            gpg_store=config.gpg_store,
        )

    with logger.log_task("Compute sha256 checksum on input files"):
        # Write input file checksums to a file that will be added to the
        # encrypted .tar.gz archive. This information must be encrypted as
        # file names sometimes contain information about their content.
        checksums = generate_checksums_file_content(
            zip(archive_paths, files_to_encrypt),
            # `max_workers` accepts only None and positive integers. Make
            # sure that zero and negative values are converted into None.
            max_workers=config.max_cpu if config.max_cpu > 0 else None,
        )
        if progress is not None:
            progress.update(0.1)

    with logger.log_task("Compress and encrypt input data [this can take a while]"):
        # Encryption is done with the recipient's public key and the optional
        # signing with the user's (i.e sender) private key. The user's private
        # key passphrase is needed to sign the encrypted file.
        encrypted_checksum_buf = io.StringIO()
        with delete_file_on_error(output_name), ZipFile(
            output_name, mode="w", compression=ZIP_STORED
        ) as zip_obj:
            with subprogress(progress, step_completion_increase=0.9) as scaled_progress:
                # Create a tar archive containing all input files
                archive_content: Tuple[ArchiveFileBase, ...] = (
                    ArchiveInMemoryFile(CHECKSUM_FILE, checksums),
                ) + tuple(
                    ArchiveFile(a_path, f)
                    for a_path, f in zip(
                        archive_paths,
                        progress_file_iter(
                            files=files_to_encrypt, mode="rb", progress=scaled_progress
                        ),
                    )
                )
                with zip_obj.open(
                    ZipInfo(DATA_FILE_ENCRYPTED, date_time=timestamp.timetuple()[:6]),
                    mode="w",
                    force_zip64=True,
                ) as fout:
                    encrypt_and_sign(
                        source=partial(
                            write_tar,
                            archive_content,
                            compress_level=compression_level,
                            compress_algo="gz",
                        ),
                        output=partial(
                            compute_checksum_on_write,
                            fout=fout,
                            checksum_buffer=encrypted_checksum_buf,
                        ),
                        gpg_store=config.gpg_store,
                        recipients_fingerprint=[
                            key.fingerprint for key in recipients_pub_key
                        ],
                        signature_fingerprint=sender_pub_key.fingerprint
                        if config.sign_encrypted_data
                        else None,
                        passphrase=enforce_passphrase(passphrase)
                        if config.sign_encrypted_data
                        else None,
                        always_trust=config.always_trust_recipient_key,
                    )
                encrypted_checksum = encrypted_checksum_buf.read()

            logger.info("Generating metadata")
            # Create a dictionary with all the info we want to store in the
            # .json file, then pass this dictionary to json.dump that will
            # convert it to a json file.
            # Use indent=4 to make the output file easier on the eye.
            metadata = MetaData(
                transfer_id=dtr_id,
                sender=HexStr1024(sender_pub_key.fingerprint),
                recipients=[HexStr1024(key.fingerprint) for key in recipients_pub_key],
                purpose=purpose,
                checksum=HexStr256(encrypted_checksum),
                compression_algorithm="gzip" if compression_level > 0 else "",
            )
            metadata_bytes, metadata_signature_bytes = byte_encode_metadata(
                metadata,
                config.gpg_store,
                passphrase,
                sender_pub_key if config.sign_encrypted_data else None,
            )

            in_memory_files = (
                (METADATA_FILE, metadata_bytes),
                (METADATA_FILE_SIG, metadata_signature_bytes),
            )
            for name, contents in in_memory_files:
                zip_obj.writestr(
                    ZipInfo(name, date_time=datetime.utcnow().timetuple()[:6]),
                    contents,
                )

    logger.info(
        "Completed data encryption: %s (%s)",
        output_name,
        get_compression_stats(total_input_file_size, os.path.getsize(output_name)),
    )
    return output_name


T = TypeVar("T")


def check_arg_value(
    arg_value: T,
    arg_name: str,
    arg_type_checker: Callable[[T], Any],
) -> None:
    """Verify that the value of variable arg_value that is named arg_name is
    following type arg_type. arg_type is a function that does a check
    of the type of the variable.
    """
    try:
        arg_type_checker(arg_value)
    except ValueError as e:
        raise UserError(f"Invalid value for argument '{arg_name}': {e}.") from e


def byte_encode_metadata(
    metadata: MetaData,
    gpg_store: gpg.GPGStore,
    passphrase: Optional[Secret[str]],
    sender_pub_key: Optional[gpg.Key],
) -> Tuple[bytes, bytes]:
    metadata_bytes = json.dumps(MetaData.asdict(metadata), indent=4).encode()
    metadata_signature_bytes = b""
    if sender_pub_key is not None:
        metadata_signature_bytes = detach_sign_file(
            metadata_bytes,
            sender_pub_key.fingerprint,
            enforce_passphrase(passphrase),
            gpg_store,
        )
    return metadata_bytes, metadata_signature_bytes


def determine_project_code(
    dtr_id: Optional[int],
    purpose: Optional[Purpose],
    portal_api: Optional[PortalApi],
    sender_pub_key: gpg.Key,
    recipients_pub_key: Iterable[gpg.Key],
) -> Optional[str]:
    if dtr_id is None:
        return None
    if purpose is None:
        raise UserError("DTR ID specified but `purpose` is missing")
    if portal_api is None:
        return None
    try:
        project_code = portal_api.verify_transfer(
            metadata=MetaData(
                transfer_id=dtr_id,
                sender=HexStr1024(sender_pub_key.fingerprint),
                recipients=[HexStr1024(key.fingerprint) for key in recipients_pub_key],
                checksum=HexStr256("0" * 64),
                purpose=purpose,
            ),
            filename="missing",
        )
        logger.info("DTR ID '%s' is valid for project '%s'", dtr_id, project_code)
    except RuntimeError as e:
        raise UserError(format(e)) from e
    return project_code


def generate_output_archive_name(output_name: Optional[str], default: str) -> str:
    """Generates the path + name of the output archive file of the encrypt
    workflow.
    If output_name does not contain any path information, the output directory
    is set to the current working directory.

    :param output_name: name or path + name of output tarball.
    :param default: default file name to use if output_name is None or
        output_name is a folder
    :return: path and name of the output tarball file.
    :raises UserError:
    """
    if output_name is None:
        output_name = default
    else:
        check_arg_value(Path(output_name).name, "output name", output_name_str)
        check_arg_value(
            Path(output_name).as_posix()
            if Path(output_name).is_dir()
            else Path(output_name).parent.as_posix(),
            "path in output name",
            output_path_str,
        )

    if Path(output_name).is_dir():
        output_name = os.path.join(output_name, default)
    # Add '.zip' extension to output name if needed.
    if not output_name.endswith(".zip"):
        output_name = output_name + ".zip"

    # If output_name does not contain any path info, the output path is
    # set to the current working directory.
    basename = Path(output_name).name
    if basename == output_name:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_name).parent

    # Verify that user has write permission to output directory. We do this
    # check now because the procedure of compression + encryption can take
    # a long time and we want to be able to warn the user immediately.
    if not output_dir.is_dir():
        raise UserError(f"output directory does not exist: {output_dir}")
    if not os.access(output_dir.as_posix(), os.W_OK):
        raise UserError(f"no write permission on directory: {output_dir}")

    return output_dir.joinpath(basename).as_posix()
