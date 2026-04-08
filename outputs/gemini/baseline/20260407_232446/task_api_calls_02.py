import requests
from unittest.mock import patch

def create_user(name, email, age):
    """
    Sends an HTTP POST request to create a new user.
    Returns the parsed JSON response as a dictionary.
    """
    url = "https://api.example.com/users"
    
    # Data to be sent in the JSON body
    payload = {
        "name": name,
        "email": email,
        "age": age
    }
    
    try:
        # The 'json' parameter automatically sets Content-Type to application/json
        # and serializes the dictionary to a JSON string.
        response = requests.post(url, json=payload)
        
        # Raise an exception for 4xx or 5xx status codes
        response.raise_for_status()
        
        # Parse and return the JSON response
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# --- Runnable Demonstration (using Mock) ---
if __name__ == "__main__":
    # Simulated successful response from the server
    mock_response_data = {
        "id": 101,
        "name": "Alice Smith",
        "email": "alice@example.com",
        "age": 30,
        "created_at": "2026-04-06T16:38:00Z"
    }

    print("Sending POST request to create user...")
    
    # We use 'patch' to simulate the API call since the URL is a placeholder
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = mock_response_data
        mock_post.return_value.status_code = 201  # Created
        
        result = create_user("Alice Smith", "alice@example.com", 30)
        
        if result:
            print("User created successfully!")
            print(f"Server Response: {result}")