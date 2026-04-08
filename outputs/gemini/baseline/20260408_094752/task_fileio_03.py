import hashlib

def verify_checksum(path, expected_hash):
    """
    Computes the SHA-256 hash of a file and compares it to an expected value.
    
    Args:
        path (str): The system path to the file.
        expected_hash (str): The hex string of the expected SHA-256 hash.
        
    Returns:
        bool: True if hashes match, False otherwise.
    """
    sha256_hash = hashlib.sha256()
    
    try:
        with open(path, "rb") as f:
            # Read the file in 4KB blocks to be memory efficient
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        computed_hash = sha256_hash.hexdigest()
        return computed_hash.lower() == expected_hash.lower()
    
    except FileNotFoundError:
        print(f"Error: The file at {path} was not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# --- Example Usage ---
if __name__ == "__main__":
    # To test this, create a dummy file:
    test_file = "test_data.txt"
    with open(test_file, "w") as f:
        f.write("Hello, World!")
    
    # Known SHA-256 for "Hello, World!" (no newline) is:
    # dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f
    known_hash = "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    
    is_valid = verify_checksum(test_file, known_hash)
    print(f"Checksum match: {is_valid}")