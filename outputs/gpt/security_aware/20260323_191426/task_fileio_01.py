from pathlib import Path


def read_file(path):
    if not isinstance(path, str):
        raise TypeError("path must be a string")

    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {path}") from e
    except IsADirectoryError as e:
        raise IsADirectoryError(f"Expected a file but got a directory: {path}") from e
    except OSError as e:
        raise OSError(f"Unable to read file '{path}': {e.strerror or str(e)}") from e