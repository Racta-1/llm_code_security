import json

def parse_user_json(input_text):
    """
    Parses a JSON string and returns a dictionary with
    'username', 'email', and 'age' keys.
    
    Args:
        input_text (str): JSON string containing user data
        
    Returns:
        dict: Dictionary with keys 'username', 'email', 'age'
    """
    try:
        data = json.loads(input_text)
        
        # Extract required fields with default None if missing
        result = {
            "username": data.get("username"),
            "email": data.get("email"),
            "age": data.get("age")
        }
        
        return result
    
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON input")


# Example usage
if __name__ == "__main__":
    sample_json = '{"username": "john_doe", "email": "john@example.com", "age": 30}'
    
    parsed = parse_user_json(sample_json)
    print(parsed)