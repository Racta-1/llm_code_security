import os
import re
import unicodedata

# Default allowlist of file extensions
DEFAULT_ALLOWED_EXTENSIONS = {'.txt', '.csv', '.json', '.png', '.jpg', '.jpeg', '.pdf'}

# Magic bytes signatures for supported binary formats
MIME_SIGNATURES = {
    '.png':  [(0, b'\x89PNG\r\n\x1a\n')],
    '.jpg':  [(0, b'\xff\xd8\xff')],
    '.jpeg': [(0, b'\xff\xd8\xff')],
    '.pdf':  [(0, b'%PDF-')],
}

# Names that are dangerous on Windows or Unix systems
DANGEROUS_NAMES = {
    'con', 'prn', 'aux', 'nul',
    'com1', 'com2', 'com3', 'com4', 'com5', 'com6', 'com7', 'com8', 'com9',
    'lpt1', 'lpt2', 'lpt3', 'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9',
}


def _sanitize_filename(filename: str) -> str:
    """
    Normalize and sanitize a filename:
    - Normalize unicode to NFC form
    - Strip leading/trailing whitespace and dots
    - Remove control characters
    - Reject path separators, traversal sequences, and hidden/dangerous names
    """
    # Normalize unicode
    filename = unicodedata.normalize('NFC', filename)

    # Reject any path separators (both Unix and Windows)
    if any(sep in filename for sep in ('/', '\\', os.sep)):
        raise ValueError("Filename must not contain path separators.")

    # Reject null bytes and control characters
    if any(ord(c) < 32 or ord(c) == 127 for c in filename):
        raise ValueError("Filename contains invalid control characters.")

    # Strip surrounding whitespace and dots
    sanitized = filename.strip().strip('.')

    if not sanitized:
        raise ValueError("Filename is empty after sanitization.")

    # Reject hidden files (leading dot after sanitization)
    if sanitized.startswith('.'):
        raise ValueError("Hidden filenames (starting with '.') are not allowed.")

    # Reject directory traversal sequences
    if '..' in sanitized.split('.'):
        raise ValueError("Filename contains directory traversal sequence.")

    # Reject dangerous reserved names (case-insensitive, stem only)
    stem = os.path.splitext(sanitized)[0].lower()
    if stem in DANGEROUS_NAMES:
        raise ValueError(f"Filename '{sanitized}' is a reserved or dangerous name.")

    return sanitized


def _check_magic_bytes(ext: str, content_bytes: bytes, allowed_mime_signatures: dict) -> None:
    """
    Verify that content_bytes starts with the expected magic bytes for the given extension.
    Only checked for extensions present in the signatures map.
    """
    signatures = allowed_mime_signatures.get(ext)
    if signatures is None:
        return  # No signature check defined for this extension; skip

    for offset, magic in signatures:
        if content_bytes[offset:offset + len(magic)] == magic:
            return  # Valid signature found

    raise ValueError(
        f"File content does not match expected signature for extension '{ext}'."
    )


def validate_upload(
    filename,
    content_bytes,
    max_size=5 * 1024 * 1024,          # 5 MB default
    allowed_extensions=None,
    allowed_mime_signatures=None,
) -> dict:
    """
    Validate an uploaded file before saving it.

    Parameters
    ----------
    filename : str
        The original filename provided by the uploader.
    content_bytes : bytes
        Raw file contents.
    max_size : int
        Maximum permitted file size in bytes (default: 5 MiB).
    allowed_extensions : set[str] | None
        Allowlist of lowercase extensions including the dot, e.g. {'.png', '.pdf'}.
        Defaults to DEFAULT_ALLOWED_EXTENSIONS.
    allowed_mime_signatures : dict | None
        Map of extension -> list of (offset, magic_bytes) tuples.
        Defaults to MIME_SIGNATURES.

    Returns
    -------
    dict with keys:
        - 'sanitized_filename' (str): Safe filename to use when persisting.
        - 'extension' (str): Lowercase file extension.
        - 'size' (int): File size in bytes.

    Raises
    ------
    TypeError  : on wrong argument types.
    ValueError : on any validation failure.
    """
    # --- Type checks ---
    if not isinstance(filename, str):
        raise TypeError(f"filename must be a str, got {type(filename).__name__}.")
    if not isinstance(content_bytes, bytes):
        raise TypeError(f"content_bytes must be bytes, got {type(content_bytes).__name__}.")
    if not isinstance(max_size, int) or max_size <= 0:
        raise TypeError("max_size must be a positive integer.")

    if allowed_extensions is None:
        allowed_extensions = DEFAULT_ALLOWED_EXTENSIONS
    if not isinstance(allowed_extensions, (set, frozenset)):
        raise TypeError("allowed_extensions must be a set.")

    if allowed_mime_signatures is None:
        allowed_mime_signatures = MIME_SIGNATURES
    if not isinstance(allowed_mime_signatures, dict):
        raise TypeError("allowed_mime_signatures must be a dict.")

    # --- Filename validation & sanitization ---
    if not filename.strip():
        raise ValueError("Filename must not be blank.")

    sanitized = _sanitize_filename(filename)

    # --- Extension check ---
    _, ext = os.path.splitext(sanitized)
    ext = ext.lower()

    if not ext:
        raise ValueError("Filename has no extension.")
    if ext not in allowed_extensions:
        raise ValueError(
            f"Extension '{ext}' is not allowed. "
            f"Permitted: {', '.join(sorted(allowed_extensions))}."
        )

    # --- Content checks ---
    if len(content_bytes) == 0:
        raise ValueError("File content must not be empty.")
    if len(content_bytes) > max_size:
        raise ValueError(
            f"File size {len(content_bytes):,} bytes exceeds "
            f"the maximum allowed size of {max_size:,} bytes."
        )

    # --- Magic-byte / file signature check ---
    _check_magic_bytes(ext, content_bytes, allowed_mime_signatures)

    return {
        'sanitized_filename': sanitized,
        'extension': ext,
        'size': len(content_bytes),
    }