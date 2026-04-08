import requests

def fetch_account_balance(account_id, api_token):
    """
    Fetch account balance from the API.

    Args:
        account_id (int or str): The account ID
        api_token (str): API authentication token

    Returns:
        dict: Parsed JSON response

    Raises:
        Exception: If the request fails
    """
    url = f"https://api.example.com/accounts/{account_id}/balance"

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)

        # Raise exception for HTTP errors (4xx, 5xx)
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching account balance: {e}")


# Example usage
if __name__ == "__main__":
    account_id = "12345"
    api_token = "your_api_token_here"

    balance_info = fetch_account_balance(account_id, api_token)
    print(balance_info)