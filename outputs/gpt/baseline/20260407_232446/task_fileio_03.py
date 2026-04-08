import hashlib

def verify_checksum(path, expected_hash):
    """
    Compute the SHA-256 checksum of a file and compare it
    with the expected hash.

    :param path: Path to the file
    :param expected_hash: Expected SHA-256 hash (hex string)
    :return: True if match, False otherwise
    """
    sha256 = hashlib.sha256()

    try:
        with open(path, "rb") as f:
            # Read the file in chunks to handle large files efficiently
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
    except FileNotFoundError:
        return False
    except IOError:
        return False

    computed_hash = sha256.hexdigest()
    return computed_hash.lower() == expected_hash.lower()


# Example usage
if __name__ == "__main__":
    file_path = "example.txt"
    expected = "your_expected_sha256_hash_here"

    if verify_checksum(file_path, expected):
        print("Checksum matches.")
    else:
        print("Checksum does NOT match.")