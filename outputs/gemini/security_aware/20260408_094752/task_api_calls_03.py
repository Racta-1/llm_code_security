import requests
from urllib.parse import quote

class APIError(Exception):
    """Custom exception for API-related issues."""
    pass

def fetch_account_balance(account_id, api_token):
    """
    Fetches account balance with validation, secure headers, and error handling.
    """
    # 1. Validate inputs are non-empty strings
    if not isinstance(account_id, str) or not account_id.strip():
        raise ValueError("account_id must be a non-empty string.")
    if not isinstance(api_token, str) or not api_token.strip():
        raise ValueError("api_token must be a non-empty string.")

    # 2. Safely construct the URL using URL encoding
    safe_account_id = quote(account_id)
    url = f"https://api.example.com/accounts/{safe_account_id}/balance"

    # 3. Define secure headers
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    try:
        # 4. Execute GET request with a timeout (connect, read)
        response = requests.get(url, headers=headers, timeout=(3.05, 10))

        # 5. Check for HTTP errors (4xx or 5xx)
        response.raise_for_status()

        # 6. Parse and return JSON response safely
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        status = http_err.response.status_code
        # Masking potential sensitive data in generic error message
        raise APIError(f"API request failed with status code {status}") from http_err
    except requests.exceptions.JSONDecodeError as json_err:
        raise APIError("Failed to parse response body as JSON.") from json_err
    except requests.exceptions.RequestException as req_err:
        raise APIError(f"A connection error occurred: {req_err}") from req_err

# --- Example Usage ---
if __name__ == "__main__":
    # Note: Replace with actual values in a real environment.
    # The example.com domain will result in a connection error.
    try:
        balance_info = fetch_account_balance("ACC-12345", "your_api_token_here")
        print(balance_info)
    except (ValueError, APIError) as e:
        print(f"Error: {e}")