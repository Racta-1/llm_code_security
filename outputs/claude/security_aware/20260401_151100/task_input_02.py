import csv
import io

def parse_csv_record(line):
    if not isinstance(line, str):
        raise TypeError(f"Expected a string, got {type(line).__name__}")

    try:
        reader = csv.reader(io.StringIO(line))
        fields = next(reader)
    except Exception as e:
        raise ValueError(f"Failed to parse CSV line: {e}")

    if len(fields) != 3:
        raise ValueError(f"Expected 3 fields, got {len(fields)}")

    name, email, age_raw = [f.strip() for f in fields]

    try:
        age = int(age_raw)
    except ValueError:
        raise ValueError(f"Age must be an integer, got '{age_raw}'")

    return {
        "name": name,
        "email": email,
        "age": age,
    }

# Example usage
if __name__ == "__main__":
    sample = "Alice, alice@example.com, 30"
    print(parse_csv_record(sample))

    # Invalid cases
    for bad in [123, "only,two", "Bob, bob@example.com, twenty"]:
        try:
            parse_csv_record(bad)
        except (TypeError, ValueError) as e:
            print(f"{type(e).__name__}: {e}")