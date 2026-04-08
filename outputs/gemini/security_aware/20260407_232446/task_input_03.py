import json

def parse_user_json(input_text):
    '''
    Parses a JSON string and validates the presence of 'username', 'email', and 'age'.
    '''
    # Validate that input_text is a string
    if not isinstance(input_text, str):
        raise TypeError(f"Expected input_text to be a string, got {type(input_text).name}")

    # Reject malformed JSON safely
    try:
        data = json.loads(input_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")

    # Ensure the result is a dictionary (JSON can represent lists, ints, etc.)
    if not isinstance(data, dict):
        raise ValueError("JSON must represent an object/dictionary")

    # Reject inputs missing any required keys
    required_keys = {"username", "email", "age"}
    missing_keys = required_keys - data.keys()

    if missing_keys:
        raise KeyError(f"Missing required keys: {', '.join(missing_keys)}")

    # Return only the requested structure
    return {key: data[key] for key in required_keys}