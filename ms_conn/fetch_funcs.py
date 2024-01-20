import requests
from .classes import Token
from config import config
import datetime

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
    
def fetch_raw_calendart_events(token: Token, start_date: datetime.datetime=None, end_date: datetime.datetime=None) -> dict:
    headers = {
        'Authorization': f'Bearer {token.access_token}',
        'Content-Type': 'application/json'
    }

    if not start_date:
        start_date = datetime.datetime.utcnow().date()
    if not end_date:
        end_date = start_date + datetime.timedelta(weeks=2)

    start_date = start_date.isoformat() + 'Z'
    end_date = end_date.isoformat() + 'Z'

    params = {
        'startDateTime': start_date,
        'endDateTime': end_date,
    }

    response = requests.get('https://graph.microsoft.com/v1.0/me/calendarView', headers=headers, params=params)

    if response.status_code == 200:
        return response.json()  # This contains the calendar events
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def fetch_tasks_in_list(token: Token, list_id):
    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{list_id}/tasks"
    headers = {
        "Authorization": f"Bearer {token.access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def fetch_task_lists(token: Token):
    url = "https://graph.microsoft.com/v1.0/me/todo/lists"
    headers = {
        "Authorization": f"Bearer {token.access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()