import os

def read_file(path):
    """
    Reads the full contents of a UTF-8 text file at the given path.

    Args:
        path (str): The file path to read.

    Returns:
        str: The full contents of the file.

    Raises:
        TypeError: If the path is not a string.
        FileNotFoundError: If the file does not exist.
        IOError: If the file cannot be read.
    """
    if not isinstance(path, str):
        raise TypeError(f"Expected a string for path, got {type(path).__name__}")
    
    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file does not exist: {path}")

    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise IOError(f"Failed to read file {path}: {e}")