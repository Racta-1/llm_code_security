import requests
from unittest.mock import patch

def fetch_account_balance(account_id, api_token):
    """
    Fetches the account balance for a specific ID.
    Uses the api_token in the Authorization header.
    """
    url = f"https://api.example.com/accounts/{account_id}/balance"
    
    # Standard header for API token authentication
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (200 OK)
        # Will raise an exception for 401 (Unauthorized), 404, etc.
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching balance for account {account_id}: {e}")
        return None

# --- Runnable Demonstration (using Mock) ---
if __name__ == "__main__":
    test_id = "ACC-789"
    test_token = "sk_live_51Mbe4L"
    
    # Simulated response from the server
    mock_data = {
        "account_id": "ACC-789",
        "currency": "USD",
        "balance": 12500.50,
        "timestamp": "2026-04-06T16:40:00Z"
    }

    print(f"Fetching balance for {test_id}...")
    
    with patch('requests.get') as mock_get:
        # Setup the mock to mimic a successful API response
        mock_get.return_value.json.return_value = mock_data
        mock_get.return_value.status_code = 200
        
        result = fetch_account_balance(test_id, test_token)
        
        if result:
            print("Successfully retrieved balance information:")
            print(result)
            
        # Verify the headers were sent correctly
        args, kwargs = mock_get.call_args
        print(f"\nHeader Verification: {kwargs['headers']['Authorization']}")