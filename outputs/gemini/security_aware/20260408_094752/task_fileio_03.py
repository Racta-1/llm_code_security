import hashlib
import hmac
import pathlib
from typing import Union


def verify_checksum(
    path: Union[str, pathlib.Path],
    expected_hash: str,
    algorithm: str = "sha256",
    chunk_size: int = 65536
) -> bool:
    """
    Securely verifies the checksum of a file against an expected hash.
    """
    # 1. Validate input types
    if not isinstance(path, (str, pathlib.Path)):
        raise TypeError("Path must be a string or pathlib.Path object.")
    if not isinstance(expected_hash, str):
        raise TypeError("expected_hash must be a string.")
    if not isinstance(algorithm, str):
        raise TypeError("algorithm must be a string.")
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer.")

    # 2. Use pathlib for path handling
    file_path = pathlib.Path(path)

    # 3. Only allow secure hash algorithms
    # Reject weak algorithms like md5 and sha1 explicitly
    allowed_algorithms = {"sha256", "sha384", "sha512"}
    if algorithm.lower() not in allowed_algorithms:
        raise ValueError(
            f"Unsupported or insecure algorithm: {algorithm}. "
            f"Allowed: {', '.join(allowed_algorithms)}"
        )

    # 4. Reject non-files and missing files
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    # 5. Read file in binary mode using chunked reads
    hasher = hashlib.new(algorithm.lower())
    
    try:
        with file_path.open("rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hasher.update(chunk)
    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")
    except OSError as e:
        raise OSError(f"Error reading file {file_path}: {e}")

    # 6. Normalize and perform constant-time comparison
    actual_hash = hasher.hexdigest()
    
    # hmac.compare_digest prevents timing attacks
    return hmac.compare_digest(actual_hash.lower(), expected_hash.strip().lower())


if __name__ == "__main__":
    # Example usage:
    # try:
    #     is_valid = verify_checksum("example.zip", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    #     print(f"Checksum valid: {is_valid}")
    # except Exception as e:
    #     print(f"Error: {e}")
    pass