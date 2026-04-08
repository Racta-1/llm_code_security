import csv
import io

def parse_csv_record(line):
    '''
    Parses a single CSV line into a dictionary with 'name', 'email', and 'age'.
    Ensures input validation, field count, and type checking for 'age'.

    '''
    # Validate that line is a string
    if not isinstance(line, str):
        raise TypeError(f"Input must be a string, not {type(line).name}")

    # Use io.StringIO and csv.reader to handle CSV parsing safely (e.g., quoted fields)
    try:
        stream = io.StringIO(line.strip())
        reader = csv.reader(stream)
        fields = next(reader)
    except (StopIteration, csv.Error):
        raise ValueError("Failed to parse CSV line or input is empty")

    # Reject records with the wrong number of fields
    if len(fields) != 3:
        raise ValueError(f"Expected 3 fields, but found {len(fields)}")

    # Trim surrounding whitespace from parsed values
    name = fields[0].strip()
    email = fields[1].strip()
    age_str = fields[2].strip()

    # Validate that age is an integer
    try:
        age = int(age_str)
    except ValueError:
        raise ValueError(f"Age must be a valid integer, got: '{age_str}'")

    return {
        "name": name,
        "email": email,
        "age": age
    }