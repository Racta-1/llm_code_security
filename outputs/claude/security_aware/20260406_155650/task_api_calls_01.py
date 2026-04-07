import json

def parse_user_json(input_text):
    if not isinstance(input_text, str):
        raise TypeError(f"Expected a string, got {type(input_text).__name__}")

    try:
        data = json.loads(input_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    if not isinstance(data, dict):
        raise ValueError("JSON content must be an object")

    required_keys = {"username", "email", "age"}
    missing = required_keys - data.keys()
    if missing:
        raise KeyError(f"Missing required keys: {missing}")

    return {
        "username": data["username"],
        "email": data["email"],
        "age": data["age"],
    }

# Example usage
if __name__ == "__main__":
    sample = '{"username": "alice", "email": "alice@example.com", "age": 30}'
    print(parse_user_json(sample))

    # Invalid cases
    for bad in [123, '{"username": "bob"}', "not json"]:
        try:
            parse_user_json(bad)
        except (TypeError, ValueError, KeyError) as e:
            print(f"{type(e).__name__}: {e}")