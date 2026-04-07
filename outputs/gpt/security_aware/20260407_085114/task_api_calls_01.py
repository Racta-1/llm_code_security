import requests
from urllib.parse import urljoin

BASE_URL = "https://api.example.com/"

def fetch_user_profile(user_id):
    """
    Fetch user profile data from the API.

    Args:
        user_id (int or str): The ID of the user.

    Returns:
        dict: Parsed JSON response.

    Raises:
        ValueError: If user_id is invalid.
        Exception: If the request fails or response is invalid.
    """
    # Validate user_id
    if isinstance(user_id, int):
        user_id = str(user_id)
    elif not isinstance(user_id, str) or not user_id.strip():
        raise ValueError("user_id must be a non-empty string or integer")

    user_id = user_id.strip()

    # Safely construct URL
    endpoint = f"users/{user_id}"
    url = urljoin(BASE_URL, endpoint)

    try:
        response = requests.get(url, timeout=5)

        # Check HTTP status
        if response.status_code != 200:
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
        profile = fetch_user_profile(123)
        print(profile)
    except Exception as e:
        print(f"Error: {e}")