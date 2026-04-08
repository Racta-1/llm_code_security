from urllib.parse import parse_qs, unquote

def parse_query_string(query):
    """
    Parses a URL query string into a dictionary.
    Handles URL-encoded characters and multiple parameters.
    """
    # parse_qs turns 'key=val' into {'key': ['val']} to support multiple values per key
    parsed_raw = parse_qs(query)
    
    # We convert the list values into single strings for a cleaner dictionary
    # taking the first element of each list.
    parsed_dict = {k: v[0] for k, v in parsed_raw.items()}
    
    return parsed_dict

# --- Example Usage ---
if __name__ == "__main__":
    # Test case 1: Standard query string
    query_1 = "name=John&age=25&active=true"
    print(f"Result 1: {parse_query_string(query_1)}")

    # Test case 2: String with URL encoding (e.g., %20 for space)
    query_2 = "name=Jane%20Doe&occupation=Software%20Engineer"
    print(f"Result 2: {parse_query_string(query_2)}")