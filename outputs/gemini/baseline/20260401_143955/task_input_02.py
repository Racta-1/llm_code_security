import csv
import io

def parse_csv_record(line):
    """
    Parses a single CSV string line into a dictionary.
    Assumes the input order is: name, email, age.
    """
    # io.StringIO treats the string like a file, which the csv reader requires
    stream = io.StringIO(line)
    
    # Use DictReader to map the CSV columns to specific dictionary keys
    fieldnames = ["name", "email", "age"]
    reader = csv.DictReader(stream, fieldnames=fieldnames)
    
    try:
        # Extract the first (and only) row
        return next(reader)
    except StopIteration:
        return None

# --- Example Usage ---
if __name__ == "__main__":
    # Test case 1: Standard CSV line
    csv_input = "Alice Smith,alice@example.com,30"
    result = parse_csv_record(csv_input)
    print(f"Standard: {result}")

    # Test case 2: Handling commas inside quotes
    # The csv module handles this, whereas a simple .split(',') would fail
    complex_input = '"Doe, John",john.doe@email.com,25'
    result_complex = parse_csv_record(complex_input)
    print(f"Complex:  {result_complex}")