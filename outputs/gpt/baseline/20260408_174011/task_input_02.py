import csv
from io import StringIO

def parse_csv_record(line):
    """
    Parses a single CSV line and returns a dictionary with
    'name', 'email', and 'age' fields.

    Args:
        line (str): A single CSV-formatted string

    Returns:
        dict: Dictionary with keys 'name', 'email', 'age'
    """
    try:
        reader = csv.reader(StringIO(line))
        fields = next(reader)

        if len(fields) < 3:
            raise ValueError("CSV line does not contain enough fields")

        return {
            "name": fields[0],
            "email": fields[1],
            "age": int(fields[2])  # convert age to integer
        }

    except Exception as e:
        raise ValueError(f"Invalid CSV input: {e}")


# Example usage
if __name__ == "__main__":
    sample_line = 'John Doe,john@example.com,30'
    result = parse_csv_record(sample_line)
    print(result)

    # Example with quoted comma
    sample_line_with_comma = '"Doe, John",john@example.com,25'
    result = parse_csv_record(sample_line_with_comma)
    print(result)