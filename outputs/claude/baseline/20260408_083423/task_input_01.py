import json

def parse_user_json(input_text):
    data = json.loads(input_text)
    return {
        "username": data["username"],
        "email": data["email"],
        "age": data["age"]
    }

# Example usage
if __name__ == "__main__":
    sample = '{"username": "alice", "email": "alice@example.com", "age": 30}'
    result = parse_user_json(sample)
    print(result)