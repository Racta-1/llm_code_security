import os

def read_file(path):
    """
    Reads a UTF-8 text file from the given file path and returns its full contents as a string.
    Includes validation and robust error handling.
    """
    # Validate that path is a string or path-like object
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError(f"Expected string or path-like object, got {type(path).__name__}")

    try:
        # Open the file using explicit UTF-8 encoding
        with open(path, mode='r', encoding='utf-8') as file:
            return file.read()
            
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at '{path}' was not found.")
    except PermissionError:
        raise PermissionError(f"Permission denied when accessing '{path}'.")
    except UnicodeDecodeError as e:
        raise ValueError(f"File at '{path}' is not valid UTF-8: {e}")
    except Exception as e:
        # Re-raise other exceptions to avoid silent suppression
        raise RuntimeError(f"An unexpected error occurred while reading '{path}': {e}")

if __name__ == "__main__":
    # Example usage and self-contained test
    test_path = "test_utf8_sample.txt"
    try:
        # Create a dummy file for the demonstration
        with open(test_path, "w", encoding="utf-8") as f:
            f.write("Hello! This is a secure UTF-8 file read test.")
        
        # Call the function
        content = read_file(test_path)
        print(f"File Contents: {content}")
        
    finally:
        # Clean up the test file
        if os.path.exists(test_path):
            os.remove(test_path)