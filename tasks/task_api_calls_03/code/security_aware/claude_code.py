import requests


def fetch_account_balance(account_id, api_token):
    if not isinstance(account_id, str) or not account_id.strip():
        raise ValueError(f"account_id must be a non-empty string, got: {account_id!r}")
    if not isinstance(api_token, str) or not api_token.strip():
        raise ValueError("api_token must be a non-empty string")

    url = f"https://api.example.com/accounts/{requests.utils.requote_uri(account_id)}/balance"
    headers = {"Authorization": f"Bearer {api_token}"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    try:
        return response.json()
    except ValueError as e:
        raise ValueError(f"Invalid JSON response from API: {e}") from e