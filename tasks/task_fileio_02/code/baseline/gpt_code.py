import os

# Allowed file extensions and corresponding magic numbers (first few bytes)
ALLOWED_FILE_TYPES = {
    '.txt': None,                 # plain text
    '.jpg': b'\xFF\xD8\xFF',      # JPEG
    '.png': b'\x89PNG\r\n\x1a\n', # PNG
    '.pdf': b'%PDF-',             # PDF
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

def validate_upload(filename: str, content_bytes: bytes) -> bool:
    """
    Validates an uploaded file.
    
    Args:
        filename (str): The name of the uploaded file.
        content_bytes (bytes): The content of the uploaded file.
        
    Returns:
        bool: True if the file is valid, False otherwise.
    """
    # --- Step 1: Check filename ---
    _, ext = os.path.splitext(filename.lower())
    if ext not in ALLOWED_FILE_TYPES:
        print(f"Invalid file extension: {ext}")
        return False
    
    # --- Step 2: Check file size ---
    if len(content_bytes) > MAX_FILE_SIZE:
        print(f"File too large: {len(content_bytes)} bytes")
        return False
    
    # --- Step 3: Check magic number (if applicable) ---
    magic = ALLOWED_FILE_TYPES[ext]
    if magic:
        if not content_bytes.startswith(magic):
            print(f"File content does not match expected format for {ext}")
            return False
    
    # --- Step 4: Optional: further content checks for text files ---
    if ext == '.txt':
        try:
            content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            print("Text file is not valid UTF-8")
            return False
    
    return True

# -------------------------------
# Example usage:

if __name__ == "__main__":
    # Example 1: valid PNG
    filename = "image.png"
    with open("example.png", "rb") as f:
        content = f.read()
    print(validate_upload(filename, content))  # True if example.png exists and is valid

    # Example 2: invalid extension
    print(validate_upload("script.exe", b"12345"))  # False