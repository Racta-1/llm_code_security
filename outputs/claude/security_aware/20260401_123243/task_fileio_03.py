import hashlib
import hmac
from pathlib import Path

ALLOWED_ALGORITHMS = {'sha256', 'sha384', 'sha512'}


def verify_checksum(path, expected_hash, algorithm="sha256", chunk_size=65536) -> bool:
    """
    Securely verify the checksum of a file.

    Parameters
    ----------
    path : str | Path
        Path to the file to verify.
    expected_hash : str
        The expected hex digest to compare against.
    algorithm : str
        Hash algorithm to use. Must be one of: sha256, sha384, sha512.
    chunk_size : int
        Number of bytes to read per chunk (default: 64 KiB).

    Returns
    -------
    bool
        True if the file's digest matches expected_hash, False otherwise.

    Raises
    ------
    TypeError   : on invalid argument types.
    ValueError  : on unsupported algorithm or malformed expected_hash.
    FileNotFoundError : if the path does not exist.
    PermissionError   : if the file cannot be read.
    IsADirectoryError : if the path points to a directory.
    """
    # --- Type validation ---
    if not isinstance(path, (str, Path)):
        raise TypeError(f"path must be a str or Path, got {type(path).__name__}.")
    if not isinstance(expected_hash, str):
        raise TypeError(f"expected_hash must be a str, got {type(expected_hash).__name__}.")
    if not isinstance(algorithm, str):
        raise TypeError(f"algorithm must be a str, got {type(algorithm).__name__}.")
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise TypeError("chunk_size must be a positive integer.")

    # --- Algorithm allowlist ---
    normalized_algorithm = algorithm.lower().strip()
    if normalized_algorithm not in ALLOWED_ALGORITHMS:
        raise ValueError(
            f"Algorithm '{algorithm}' is not allowed. "
            f"Choose one of: {', '.join(sorted(ALLOWED_ALGORITHMS))}."
        )

    # --- Normalize and validate the expected hash ---
    normalized_hash = expected_hash.strip().lower()
    if not normalized_hash:
        raise ValueError("expected_hash must not be blank.")
    if not all(c in '0123456789abcdef' for c in normalized_hash):
        raise ValueError("expected_hash contains non-hexadecimal characters.")

    expected_digest_length = hashlib.new(normalized_algorithm).digest_size * 2
    if len(normalized_hash) != expected_digest_length:
        raise ValueError(
            f"expected_hash length {len(normalized_hash)} is invalid for "
            f"{normalized_algorithm} (expected {expected_digest_length} hex characters)."
        )

    # --- Path validation ---
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"No such file or directory: '{file_path}'.")
    if file_path.is_dir():
        raise IsADirectoryError(f"Path is a directory, not a file: '{file_path}'.")
    if not file_path.is_file():
        raise ValueError(f"Path does not point to a regular file: '{file_path}'.")

    # --- Chunked binary read and digest computation ---
    hasher = hashlib.new(normalized_algorithm)

    try:
        with file_path.open('rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
    except PermissionError as e:
        raise PermissionError(f"Permission denied reading file: '{file_path}'.") from e

    actual_digest = hasher.hexdigest()

    # --- Constant-time comparison to prevent timing attacks ---
    return hmac.compare_digest(actual_digest, normalized_hash)