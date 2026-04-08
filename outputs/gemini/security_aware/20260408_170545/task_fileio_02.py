import os
import re
import unicodedata
import binascii
from typing import List, Optional, Dict

class FileValidationError(ValueError):
    """Custom exception for file validation failures."""
    pass

def validate_upload(
    filename: str, 
    content_bytes: bytes, 
    max_size: int = 5242880, 
    allowed_extensions: Optional[List[str]] = None,
    allowed_mime_signatures: Optional[Dict[str, bytes]] = None
) -> str:
    """
    Validates an uploaded file's metadata and content for security and integrity.
    
    Returns:
        str: A sanitized, safe version of the filename if valid.
        
    Raises:
        TypeError: If input types are incorrect.
        FileValidationError: If validation fails for security or size reasons.
    """
    
    # 1. Strict Input Type Validation
    if not isinstance(filename, str):
        raise TypeError("Filename must be a string")
    if not isinstance(content_bytes, bytes):
        raise TypeError("Content must be bytes")
    if not isinstance(max_size, int):
        raise TypeError("Max size must be an integer")

    # 2. File Content Checks (Size and Presence)
    file_size = len(content_bytes)
    if file_size == 0:
        raise FileValidationError("File is empty")
    if file_size > max_size:
        raise FileValidationError(f"File size {file_size} exceeds limit of {max_size} bytes")

    # 3. Filename Sanitization and Normalization
    # Normalize unicode to prevent bypasses using visually similar characters
    filename = unicodedata.normalize('NFKC', filename)
    
    # Remove directory components to prevent traversal
    basename = os.path.basename(filename)
    
    if not basename or basename in ('.', '..'):
        raise FileValidationError("Invalid or empty filename")

    # Reject control characters and path separators
    if re.search(r'[\x00-\x1f\x7f\\/\s]', basename):
        raise FileValidationError("Filename contains invalid characters or path separators")

    # Sanitize: Allow only alphanumeric, dots, underscores, and hyphens
    # This prevents shell injection and hidden file tricks
    sanitized_name = re.sub(r'[^\w\.\-]', '_', basename)
    
    # Ensure it doesn't start with a dot (hidden file)
    if sanitized_name.startswith('.'):
        sanitized_name = f"upload_{sanitized_name.lstrip('.')}"

    # 4. Extension Validation
    if allowed_extensions is None:
        allowed_extensions = ['.txt', '.csv', '.json', '.png', '.jpg', '.jpeg', '.pdf']
    
    ext = os.path.splitext(sanitized_name)[1].lower()
    if ext not in [e.lower() for e in allowed_extensions]:
        raise FileValidationError(f"Extension '{ext}' is not allowed")

    # 5. Magic Bytes / Signature Verification
    # Mapping of extension to expected hex header
    signatures = {
        '.png': b'\x89PNG\r\n\x1a\n',
        '.jpg': b'\xff\xd8\xff',
        '.jpeg': b'\xff\xd8\xff',
        '.pdf': b'%PDF-',
    }
    
    # Merge custom signatures if provided
    if allowed_mime_signatures:
        signatures.update(allowed_mime_signatures)

    if ext in signatures:
        expected_sig = signatures[ext]
        if not content_bytes.startswith(expected_sig):
            raise FileValidationError(f"File signature mismatch for {ext}")

    # JSON basic structural check (if applicable)
    if ext == '.json':
        import json
        try:
            json.loads(content_bytes.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise FileValidationError("Invalid JSON content")

    return sanitized_name

# Example Usage / Test
if __name__ == "__main__":
    try:
        # Valid Case
        valid_name = validate_upload("my_photo.png", b"\x89PNG\r\n\x1a\nSomeData")
        print(f"Validated successfully: {valid_name}")
        
        # Traversal Attempt
        # validate_upload("../../etc/passwd", b"data") # Raises FileValidationError
        
        # Signature Mismatch
        # validate_upload("virus.png", b"NOT_A_PNG") # Raises FileValidationError
        
    except (FileValidationError, TypeError) as e:
        print(f"Validation failed: {e}")