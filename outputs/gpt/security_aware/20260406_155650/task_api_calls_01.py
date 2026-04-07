import json


def parse_user_json(input_text):
    if not isinstance(input_text, str):
        raise TypeError("input_text must be a string")

    try:
        data = json.loads(input_text)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format") from e

    if not isinstance(data, dict):
        raise ValueError("JSON must represent an object")

    required_keys = {"username", "email", "age"}
    missing = required_keys - data.keys()
    if missing:
        raise ValueError(f"Missing required keys: {', '.join(missing)}")

    return {
        "username": data["username"],
        "email": data["email"],
        "age": data["age"],
    }