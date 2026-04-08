import requests

def fetch_user_profile(user_id):
    url = f"https://api.example.com/users/{user_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()