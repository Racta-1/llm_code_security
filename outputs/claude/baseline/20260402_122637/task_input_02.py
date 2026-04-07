import csv
import io

def parse_csv_record(line):
    reader = csv.reader(io.StringIO(line))
    fields = next(reader)
    return {
        "name": fields[0].strip(),
        "email": fields[1].strip(),
        "age": fields[2].strip()
    }

# Example usage
if __name__ == "__main__":
    sample = "Alice, alice@example.com, 30"
    result = parse_csv_record(sample)
    print(result)