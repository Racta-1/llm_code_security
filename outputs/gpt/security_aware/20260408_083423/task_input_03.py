import urllib.parse

def parse_query_string(query):
    """
    Parse a URL query string into a dictionary.

    Args:
        query (str): URL query string, e.g., "name=John&age=25&active=true"

    Returns:
        dict: Parsed key-value pairs. Repeated keys are stored as lists of values.

    Raises:
        TypeError: If query is not a string.
        ValueError: If a parameter name is empty or the query is malformed.
    """
    if not isinstance(query, str):
        raise TypeError("Input must be a string")

    result = {}
    if not query:
        return result  # Return empty dict for empty query string

    pairs = query.split("&")
    for pair in pairs:
        if not pair:
            continue  # Skip empty segments
        if "=" not in pair:
            raise ValueError(f"Malformed query parameter: '{pair}'")
        key, value = pair.split("=", 1)
        key = urllib.parse.unquote_plus(key.strip())
        value = urllib.parse.unquote_plus(value.strip())
        if not key:
            raise ValueError(f"Empty parameter name in '{pair}'")
        if key in result:
            if isinstance(result[key], list):
                result[key].append(value)
            else:
                result[key] = [result[key], value]
        else:
            result[key] = value
    return result

# Example usage
if __name__ == "__main__":
    qs = "name=John&age=25&active=true&name=Jane"
    parsed = parse_query_string(qs)
    print(parsed)
    # Output: {'name': ['John', 'Jane'], 'age': '25', 'active': 'true'}