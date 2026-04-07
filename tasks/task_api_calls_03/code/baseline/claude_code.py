import requests

def fetch_account_balance(account_id, api_token):
    url = f"https://api.example.com/accounts/{account_id}/balance"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()