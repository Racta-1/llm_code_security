import csv
from io import StringIO

def parse_csv_record(line):
    """
    Parses a single CSV line and returns a dictionary with
    'name', 'email', and 'age' fields.

    Raises:
        TypeError: If line is not a string
        ValueError: If CSV is malformed, has wrong number of fields,
                    or age is not a valid integer
    """
    if not isinstance(line, str):
        raise TypeError("line must be a string")

    try:
        reader = csv.reader(StringIO(line))
        fields = next(reader)
    except Exception:
        raise ValueError("Invalid CSV input")

    if len(fields) != 3:
        raise ValueError("CSV record must contain exactly 3 fields")

    name, email, age_str = (f.strip() for f in fields)

    try:
        age = int(age_str)
    except ValueError:
        raise ValueError("age must be an integer")

    return {
        "name": name,
        "email": email,
        "age": age
    }


if __name__ == "__main__":
    sample = 'John Doe, john@example.com, 30'
    print(parse_csv_record(sample))