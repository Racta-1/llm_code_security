import requests
from urllib.parse import quote

class APIError(Exception):
    """Custom exception for API-related failures."""
    pass

def fetch_user_profile(user_id):
    """
    Fetches a user profile from the API with validation, safety, and timeouts.
    """
    # 1. Validate user_id
    if not isinstance(user_id, (str, int)) or (isinstance(user_id, str) and not user_id.strip()):
        raise ValueError("user_id must be a non-empty string or an integer.")

    # 2. Safely construct the URL
    # URL encoding ensures that special characters in user_id don't break the URL structure
    safe_user_id = quote(str(user_id))
    url = f"https://api.example.com/users/{safe_user_id}"

    try:
        # 3. Send GET request with a timeout (connect, read) in seconds
        response = requests.get(url, timeout=(3.05, 10))

        # 4. Check HTTP status code
        # Returns 200 for OK, raises HTTPError for 4xx or 5xx
        response.raise_for_status()

        # 5. Parse JSON safely
        # requests.json() raises requests.exceptions.JSONDecodeError if body is not valid JSON
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        raise APIError(f"HTTP error occurred: {http_err.response.status_code} - {http_err.response.text}") from http_err
    except requests.exceptions.JSONDecodeError as json_err:
        raise APIError("Failed to parse response as JSON.") from json_err
    except requests.exceptions.RequestException as req_err:
        raise APIError(f"A network or connection error occurred: {req_err}") from req_err

# --- Example Usage ---
if __name__ == "__main__":
    # Note: Since api.example.com is a placeholder, this block demonstrates 
    # the function's structure. In a real environment, it would return a dictionary.
    try:
        profile = fetch_user_profile(12345)
        print(profile)
    except Exception as e:
        print(f"Error: {e}")