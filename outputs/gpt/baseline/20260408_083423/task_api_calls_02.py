import requests

def create_user(name, email, age):
    """
    Create a new user via API.

    Args:
        name (str): User's name
        email (str): User's email
        age (int): User's age

    Returns:
        dict: Parsed JSON response

    Raises:
        Exception: If the request fails
    """
    url = "https://api.example.com/users"
    
    payload = {
        "name": name,
        "email": email,
        "age": age
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Raise error for bad HTTP status codes
        response.raise_for_status()
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error creating user: {e}")


# Example usage
if __name__ == "__main__":
    new_user = create_user("Alice", "alice@example.com", 25)
    print(new_user)