import requests

def create_user(name, email, age):
    url = "https://api.example.com/users"
    payload = {
        "name": name,
        "email": email,
        "age": age
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()