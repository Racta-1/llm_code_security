import os


def read_file(path):
    if not isinstance(path, str):
        raise TypeError(f"path must be a string, got {type(path).__name__}")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"No such file or directory: '{path}'")
    
    if not os.path.isfile(path):
        raise ValueError(f"Path is not a file: '{path}'")
    
    with open(path, encoding="utf-8") as f:
        return f.read()