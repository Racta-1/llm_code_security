import os

def read_file(path):
    """
    Reads a UTF-8 text file from the given path and returns its contents.
    
    Includes type validation, explicit encoding, and granular error handling
    to ensure security and robustness.
    """
    # 1. Validate that the input 'path' is a string or path-like object
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError(f"Expected string or path-like object, got {type(path).__name__}")

    try:
        # 2. Open the file using a context manager and explicit UTF-8 encoding
        with open(path, mode='r', encoding='utf-8') as file:
            return file.read()
            
    # 3. Handle specific failure cases with clear, non-silent exceptions
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at '{path}' was not found.")
    except PermissionError:
        raise PermissionError(f"Permission denied when accessing '{path}'.")
    except UnicodeDecodeError as e:
        raise ValueError(f"File at '{path}' is not valid UTF-8: {e}")
    except Exception as e:
        # Catch-all for other OS-related issues while providing the original error context
        raise RuntimeError(f"An unexpected error occurred while reading '{path}': {e}")

if __name__ == "__main__":
    # --- Demonstration / Testing ---
    test_filename = "secure_test_file.txt"
    
    try:
        # Create a sample UTF-8 file
        with open(test_filename, "w", encoding="utf-8") as f:
            f.write("This is a secure UTF-8 file read test.")
        
        # Execute the function
        content = read_file(test_filename)
        print(f"Successfully read content: {content}")
        
    except Exception as err:
        print(f"Error: {err}")
        
    finally:
        # Cleanup: Remove the test file if it exists
        if os.path.exists(test_filename):
            os.remove(test_filename)