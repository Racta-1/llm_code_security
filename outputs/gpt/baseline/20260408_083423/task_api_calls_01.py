import requests

def fetch_user_profile(user_id):
    """
    Fetch user profile data from the API.

    Args:
        user_id (int or str): The ID of the user.

    Returns:
        dict: Parsed JSON response.

    Raises:
        Exception: If the request fails or returns a non-200 status code.
    """
    url = f"https://api.example.com/users/{user_id}"
    
    try:
        response = requests.get(url)
        
        # Raise an error for bad status codes (4xx, 5xx)
        response.raise_for_status()
        
        # Parse and return JSON
        return response.json()
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching user profile: {e}")