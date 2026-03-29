def read_file(path):
    """
    Reads a UTF-8 encoded text file and returns its full contents as a string.

    :param path: Path to the file
    :return: File contents as a string
    """
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


# Example usage
if __name__ == "__main__":
    file_path = "example.txt"  # Replace with your file path
    try:
        contents = read_file(file_path)
        print(contents)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")