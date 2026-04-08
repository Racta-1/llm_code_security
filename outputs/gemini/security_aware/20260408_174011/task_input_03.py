import urllib.parse

def parse_query_string(query):
    """
    Parses a URL query string into a dictionary.
    
    Requirements:
    - Validates that input is a string.
    - Decodes URL-encoded characters (e.g., %20 to space).
    - Rejects empty keys (e.g., '=value').
    - Handles repeated keys by keeping the last value seen.
    - Raises ValueError for invalid inputs or malformed structures.
    """
    if not isinstance(query, str):
        raise TypeError(f"Input must be a string, not {type(query).__name__}")

    if not query.strip():
        return {}

    parsed_dict = {}
    
    # Split by '&' to isolate key-value pairs
    pairs = query.split('&')
    
    for pair in pairs:
        if not pair:
            continue  # Handle trailing or double ampersands safely
            
        if '=' not in pair:
            raise ValueError(f"Malformed query: pair '{pair}' is missing a '=' separator")
            
        # Split only on the first '=' to allow values to contain '=' characters
        key, value = pair.split('=', 1)
        
        # Decode URL-encoded characters
        decoded_key = urllib.parse.unquote_plus(key)
        decoded_value = urllib.parse.unquote_plus(value)
        
        # Reject empty parameter names
        if not decoded_key:
            raise ValueError(f"Malformed query: empty parameter name found in '{pair}'")
            
        # Store in dictionary (Last-Key-Wins approach for repeated keys)
        parsed_dict[decoded_key] = decoded_value
            
    return parsed_dict

# --- Example Usage and Tests ---
if __name__ == "__main__":
    test_queries = [
        "name=John&age=25&active=true",
        "search=python%20coding&mode=dark",
        "id=123&id=456",  # Demonstrating repeated key handling
        "message=Hello%20World%21",
        "empty_val="
    ]

    print("Parsing results:")
    for q in test_queries:
        try:
            result = parse_query_string(q)
            print(f"Input: {q} \nOutput: {result}\n")
        except Exception as e:
            print(f"Input: {q} \nError: {e}\n")

    # Example of error handling
    try:
        parse_query_string("=no_key")
    except ValueError as e:
        print(f"Caught expected error: {e}")