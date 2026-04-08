import requests

def fetch_user_profile(user_id):
    if not isinstance(user_id, (str, int)) or (isinstance(user_id, str) and not user_id.strip()):
        raise ValueError(f"user_id must be a non-empty string or integer, got: {user_id!r}")

    url = f"https://api.example.com/users/{requests.utils.requote_uri(str(user_id))}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    try:
        return response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON response from API: {e}") from e