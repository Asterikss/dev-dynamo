import requests
from .classes import Token
from config import config

def fetch_raw_emails(token: Token, num_emails: int = 10, unread: bool = False):
    headers = {
        'Authorization': f'Bearer {token.access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        '$top': num_emails
    }
    if unread:
        params["$filter"] = "isRead eq false"

    response = requests.get(config.ms.url.mails, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return {}