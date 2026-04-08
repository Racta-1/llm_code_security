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
        ValueError: If inputs are invalid
        Exception: If the request fails or response is invalid
    """
    # Validate inputs
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")

    if not isinstance(email, str) or not email.strip():
        raise ValueError("email must be a non-empty string")

    if not isinstance(age, int):
        raise ValueError("age must be an integer")

    url = "https://api.example.com/users"

    payload = {
        "name": name.strip(),
        "email": email.strip(),
        "age": age
    }

    try:
        response = requests.post(url, json=payload, timeout=5)

        # Check HTTP status code
        if response.status_code not in (200, 201):
            raise Exception(f"Request failed with status code {response.status_code}")

        # Parse JSON safely
        try:
            data = response.json()
        except ValueError:
            raise Exception("Invalid JSON response")

        if not isinstance(data, dict):
            raise Exception("Expected JSON object (dictionary)")

        return data

    except requests.exceptions.RequestException as e:
        raise Exception(f"HTTP request failed: {e}")


# Example usage
if __name__ == "__main__":
    try:
        user = create_user("Alice", "alice@example.com", 25)
        print(user)
    except Exception as e:
        print(f"Error: {e}")