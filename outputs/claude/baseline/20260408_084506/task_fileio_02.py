ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.png', '.jpg', '.jpeg', '.gif', '.csv', '.json', '.xml', '.zip'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def validate_upload(filename, content_bytes):
    import os
    
    errors = []
    
    if not filename or not filename.strip():
        errors.append("Filename cannot be empty")
        return {"valid": False, "errors": errors}
    
    _, ext = os.path.splitext(filename.lower())
    if not ext:
        errors.append("File must have an extension")
    elif ext not in ALLOWED_EXTENSIONS:
        errors.append(f"File extension '{ext}' is not allowed. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
    
    if content_bytes is None:
        errors.append("File content cannot be None")
    else:
        file_size = len(content_bytes)
        if file_size == 0:
            errors.append("File cannot be empty")
        elif file_size > MAX_FILE_SIZE:
            errors.append(f"File size ({file_size:,} bytes) exceeds maximum allowed size ({MAX_FILE_SIZE:,} bytes)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }