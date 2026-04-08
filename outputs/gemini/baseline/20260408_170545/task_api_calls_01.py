import requests
from unittest.mock import patch

def fetch_user_profile(user_id):
    """
    Sends an HTTP GET request to fetch a user profile and returns 
    the parsed JSON response.
    """
    url = f"https://api.example.com/users/{user_id}"
    
    try:
        response = requests.get(url)
        
        # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        response.raise_for_status()
        
        # Return the parsed JSON as a dictionary
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching user {user_id}: {e}")
        return None

# --- Mocking the environment for a runnable demonstration ---
if __name__ == "__main__":
    # We use a mock to simulate the API response since example.com doesn't exist
    mock_data = {
        "id": 123,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "status": "active"
    }

    print("Simulating API call...")
    with patch('requests.get') as mock_get:
        # Configure the mock to return a response-like object
        mock_get.return_value.json.return_value = mock_data
        mock_get.return_value.status_code = 200
        
        # Execute the function
        user_profile = fetch_user_profile(123)
        
        if user_profile:
            print("Successfully fetched profile:")
            print(user_profile)