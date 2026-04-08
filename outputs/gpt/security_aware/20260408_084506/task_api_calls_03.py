import requests
from urllib.parse import urljoin

BASE_URL = "https://api.example.com/"

def fetch_account_balance(account_id, api_token):
    """
    Fetch account balance from the API.

    Args:
        account_id (str): The account ID
        api_token (str): API authentication token

    Returns:
        dict: Parsed JSON response

    Raises:
        ValueError: If inputs are invalid
        Exception: If the request fails or response is invalid
    """
    # Validate inputs
    if not isinstance(account_id, str) or not account_id.strip():
        raise ValueError("account_id must be a non-empty string")

    if not isinstance(api_token, str) or not api_token.strip():
        raise ValueError("api_token must be a non-empty string")

    account_id = account_id.strip()
    api_token = api_token.strip()

    # Safely construct URL
    endpoint = f"accounts/{account_id}/balance"
    url = urljoin(BASE_URL, endpoint)

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)

        # Check HTTP status code
        if response.status_code < 200 or response.status_code >= 300:
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
        balance = fetch_account_balance("12345", "your_api_token_here")
        print(balance)
    except Exception as e:
        print(f"Error: {e}")