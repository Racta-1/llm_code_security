from urllib.parse import parse_qs, urlencode

def parse_query_string(query):
    parsed = parse_qs(query, keep_blank_values=True)
    return {key: values[0] for key, values in parsed.items()}

# Example usage
if __name__ == "__main__":
    sample = "name=John&age=25&active=true"
    result = parse_query_string(sample)
    print(result)