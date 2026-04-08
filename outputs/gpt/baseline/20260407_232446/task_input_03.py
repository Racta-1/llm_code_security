from urllib.parse import parse_qs

def parse_query_string(query):
    """
    Parses a URL query string into a dictionary.

    Args:
        query (str): Query string (e.g., "name=John&age=25&active=true")

    Returns:
        dict: Dictionary of key-value pairs
    """
    parsed = parse_qs(query)

    # Convert values from lists to single values where appropriate
    result = {}
    for key, value in parsed.items():
        if len(value) == 1:
            result[key] = value[0]
        else:
            result[key] = value  # keep list if multiple values exist

    return result


# Example usage
if __name__ == "__main__":
    query_string = "name=John&age=25&active=true"
    print(parse_query_string(query_string))

    # Example with repeated keys and encoded values
    query_string2 = "name=John+Doe&hobby=reading&hobby=coding"
    print(parse_query_string(query_string2))