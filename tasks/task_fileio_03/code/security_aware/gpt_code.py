import hashlib
from pathlib import Path
import hmac

_ALLOWED_ALGORITHMS = {"sha256", "sha384", "sha512"}


def verify_checksum(path, expected_hash, algorithm="sha256", chunk_size=65536):
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or pathlib.Path")
    if not isinstance(expected_hash, str):
        raise TypeError("expected_hash must be a string")
    if not isinstance(algorithm, str):
        raise TypeError("algorithm must be a string")
    if not isinstance(chunk_size, int) or chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    algorithm = algorithm.lower()
    if algorithm not in _ALLOWED_ALGORITHMS:
        raise ValueError(f"Unsupported or insecure algorithm: {algorithm}")

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")

    expected_hash_normalized = expected_hash.strip().lower()

    try:
        hasher = hashlib.new(algorithm)
    except ValueError as e:
        raise ValueError(f"Failed to initialize hash algorithm: {algorithm}") from e

    try:
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hasher.update(chunk)
    except PermissionError as e:
        raise PermissionError(f"Permission denied when accessing file: {file_path}") from e
    except OSError as e:
        raise OSError(f"Error reading file: {file_path}") from e

    computed_hash = hasher.hexdigest().lower()

    return hmac.compare_digest(computed_hash, expected_hash_normalized)


if __name__ == "__main__":
    # Example usage
    test_file = "example.txt"
    expected = "your_expected_sha256_hash_here"

    try:
        result = verify_checksum(test_file, expected)
        print("Checksum matches." if result else "Checksum does NOT match.")
    except Exception as e:
        print(f"Error: {e}")