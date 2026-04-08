import os
import re
import unicodedata


DEFAULT_ALLOWED_EXTENSIONS = {
    ".txt", ".csv", ".json", ".png", ".jpg", ".jpeg", ".pdf"
}

DEFAULT_MIME_SIGNATURES = {
    ".png": [b"\x89PNG\r\n\x1a\n"],
    ".jpg": [b"\xff\xd8\xff"],
    ".jpeg": [b"\xff\xd8\xff"],
    ".pdf": [b"%PDF"],
    ".txt": [],
    ".csv": [],
    ".json": [],
}


_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")
_INVALID_NAME = re.compile(r"[^A-Za-z0-9._-]")


def _sanitize_filename(filename: str) -> str:
    filename = unicodedata.normalize("NFKC", filename)

    if _CONTROL_CHARS.search(filename):
        raise ValueError("Filename contains control characters")

    if "/" in filename or "\\" in filename:
        raise ValueError("Filename must not contain path separators")

    filename = filename.strip()

    if not filename:
        raise ValueError("Filename is empty")

    if filename in {".", ".."}:
        raise ValueError("Invalid filename")

    name = os.path.basename(filename)

    if name.startswith("."):
        raise ValueError("Hidden filenames are not allowed")

    if name != filename:
        raise ValueError("Invalid filename path components")

    name = _INVALID_NAME.sub("_", name)

    if not name or name in {".", ".."}:
        raise ValueError("Filename became invalid after sanitization")

    return name


def _validate_signature(ext: str, content: bytes, signatures: dict):
    sigs = signatures.get(ext, [])
    if not sigs:
        return

    if not any(content.startswith(sig) for sig in sigs):
        raise ValueError(f"File signature does not match extension {ext}")


def validate_upload(
    filename,
    content_bytes,
    max_size=5242880,
    allowed_extensions=None,
    allowed_mime_signatures=None,
):
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")

    if not isinstance(content_bytes, (bytes, bytearray)):
        raise TypeError("content_bytes must be bytes or bytearray")

    if not isinstance(max_size, int) or max_size <= 0:
        raise TypeError("max_size must be a positive integer")

    if allowed_extensions is None:
        allowed_extensions = DEFAULT_ALLOWED_EXTENSIONS
    else:
        if not isinstance(allowed_extensions, (set, list, tuple)):
            raise TypeError("allowed_extensions must be a collection of strings")
        allowed_extensions = {str(ext).lower() for ext in allowed_extensions}

    if allowed_mime_signatures is None:
        allowed_mime_signatures = DEFAULT_MIME_SIGNATURES
    else:
        if not isinstance(allowed_mime_signatures, dict):
            raise TypeError("allowed_mime_signatures must be a dict")

    safe_name = _sanitize_filename(filename)

    base, ext = os.path.splitext(safe_name.lower())

    if not ext:
        raise ValueError("File must have an extension")

    if ext not in allowed_extensions:
        raise ValueError(f"Extension '{ext}' is not allowed")

    size = len(content_bytes)

    if size == 0:
        raise ValueError("File is empty")

    if size > max_size:
        raise ValueError("File exceeds maximum allowed size")

    _validate_signature(ext, content_bytes, allowed_mime_signatures)

    if ext in {".txt", ".csv", ".json"}:
        try:
            content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError(f"{ext} files must be UTF-8 encoded")

    return {
        "sanitized_filename": safe_name,
        "extension": ext,
        "size": size,
        "valid": True,
    }


if __name__ == "__main__":
    sample = b"\x89PNG\r\n\x1a\nexample"
    result = validate_upload("test_image.png", sample)
    print(result)