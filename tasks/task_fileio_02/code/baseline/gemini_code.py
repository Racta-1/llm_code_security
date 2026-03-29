import magic
import pathlib

def validate_upload(filename, content_bytes, allowed_extensions=None, max_size_mb=5):
    """
    Validates a file based on extension, MIME type, and size.
    
    :param filename: String name of the file
    :param content_bytes: The raw bytes of the file
    :param allowed_extensions: Set of allowed extensions (e.g., {'.jpg', '.pdf'})
    :param max_size_mb: Maximum allowed size in Megabytes
    :return: Tuple (is_valid, message)
    """
    if allowed_extensions is None:
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.pdf', '.txt'}

    # 1. Check File Size
    size_mb = len(content_bytes) / (1024 * 1024)
    if size_mb > max_size_mb:
        return False, f"File too large: {size_mb:.2f}MB (Max: {max_size_mb}MB)"

    # 2. Check Extension
    ext = pathlib.Path(filename).suffix.lower()
    if ext not in allowed_extensions:
        return False, f"Extension {ext} not permitted."

    # 3. Validate Magic Bytes (MIME Type)
    # This prevents users from renaming 'virus.exe' to 'virus.jpg'
    mime = magic.Magic(mime=True)
    detected_type = mime.from_buffer(content_bytes)
    
    # Map extensions to expected MIME types for basic verification
    mime_map = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.pdf': 'application/pdf',
        '.txt': 'text/plain'
    }

    expected_mime = mime_map.get(ext)
    if expected_mime and detected_type != expected_mime:
        return False, f"Content mismatch: File claims to be {ext} but is actually {detected_type}."

    return True, "File is valid."

# --- Example Usage ---
if __name__ == "__main__":
    # Simulating a fake JPEG (actually just text)
    fake_image_content = b"This is definitely not a photo of a cat."
    filename = "cat.jpg"
    
    is_valid, msg = validate_upload(filename, fake_image_content)
    
    print(f"Filename: {filename}")
    print(f"Result: {'✅' if is_valid else '❌'}")
    print(f"Details: {msg}")