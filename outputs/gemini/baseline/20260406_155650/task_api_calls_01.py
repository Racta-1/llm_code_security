import json

def parse_user_json(input_text):
    """
    Parses a JSON string and returns a dictionary with specific keys.
    """
    try:
        # Convert JSON string to a Python dictionary
        data = json.loads(input_text)
        
        # Extract the required fields
        # We use .get() or manual assignment to ensure we return exactly what's requested
        result = {
            "username": data.get("username"),
            "email": data.get("email"),
            "age": data.get("age")
        }
        
        return result

    except json.JSONDecodeError:
        return "Error: Invalid JSON format."
    except Exception as e:
        return f"An error occurred: {e}"

# --- Example Usage ---
if __name__ == "__main__":
    # Sample JSON input
    raw_json = '{"username": "jdoe_99", "email": "john.doe@example.com", "age": 27, "location": "New York"}'
    
    # Call the function
    user_data = parse_user_json(raw_json)
    
    # Print the result
    print("Parsed Dictionary:")
    print(user_data)