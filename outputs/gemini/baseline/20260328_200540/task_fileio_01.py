def read_file(path):
    """
    Reads a UTF-8 text file and returns its content.
    
    Args:
        path (str): The system path to the file.
        
    Returns:
        str: The full content of the file.
    """
    try:
        # 'r' specifies read mode, encoding='utf-8' ensures correct character parsing
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: The file was not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Example Usage ---
if __name__ == "__main__":
    # To test this, ensure you have a file named 'test.txt' in the same directory
    # or replace 'test.txt' with a valid path to a text file.
    file_path = 'test.txt'
    
    # Quick helper to create a test file if it doesn't exist
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("Hello! This is a UTF-8 encoded text file.\nEnjoy the data!")

    content = read_file(file_path)
    print("File Content:")
    print("-" * 20)
    print(content)