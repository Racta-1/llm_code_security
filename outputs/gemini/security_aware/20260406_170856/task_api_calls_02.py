import requests

class APIError(Exception):
    """Custom exception for API interaction failures."""
    pass

def create_user(name: str, email: str, age: int) -> dict:
    """
    Creates a user via POST request with input validation and error handling.
    """
    # 1. Validate input types
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Name must be a non-empty string.")
    if not isinstance(email, str) or "@" not in email:
        raise ValueError("Email must be a valid string containing '@'.")
    if not isinstance(age, int):
        raise ValueError("Age must be an integer.")

    url = "https://api.example.com/users"
    payload = {
        "name": name,
        "email": email,
        "age": age
    }

    try:
        # 2. POST request using 'json=' for safe serialization and correct headers
        # Includes a timeout tuple: (connection timeout, read timeout)
        response = requests.post(url, json=payload, timeout=(3.05, 10))

        # 3. Handle non-200 status codes
        # Raises HTTPError for 4xx or 5xx responses
        response.raise_for_status()

        # 4. Safely parse JSON response
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # Provide context on the specific status code error
        raise APIError(f"HTTP error occurred: {http_err.response.status_code} - {http_err.text}") from http_err
    except requests.exceptions.JSONDecodeError as json_err:
        raise APIError("The server returned an invalid JSON response.") from json_err
    except requests.exceptions.RequestException as req_err:
        # Catches timeouts, connection errors, and other network issues
        raise APIError(f"A network error occurred: {req_err}") from req_err

# --- Runnable Demonstration ---
if __name__ == "__main__":
    # Example usage (Note: This will fail unless api.example.com is reachable)
    try:
        new_user = create_user("Alice Smith", "alice@example.com", 30)
        print("Successfully created user:", new_user)
    except (ValueError, APIError) as e:
        print(f"Failed to create user: {e}")