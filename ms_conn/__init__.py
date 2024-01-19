from typing import Dict, List
import streamlit as st
import requests
from urllib.parse import urlencode
from config import config
import datetime
from .classes import Token
from .fetch_funcs import fetch_raw_emails
from pprint import pprint

from bs4 import BeautifulSoup

def extract_text_from_html(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    text = soup.get_text(separator=' ', strip=True)
    return text

def generate_auth_url() -> str:
    params = {
        'client_id': config.ms.client_id,
        'response_type': 'code',
        'redirect_uri': config.ms.redirect_uri,
        'scope': config.ms.scope,
        'response_mode': 'query'
    }
    return f'{config.ms.url.auth}?{urlencode(params)}'

def exchange_code_for_token(code: str) -> dict:
    data = {
        'client_id': config.ms.client_id,
        'scope': config.ms.scope,
        'code': code,
        'redirect_uri': config.ms.redirect_uri,
        'grant_type': 'authorization_code',
        'client_secret': config.ms.client_secret
    }
    response = requests.post(config.ms.url.token, data=data)
    return response.json()

def get_user_emails(token: Token, num_emails: int = 10, unread: bool = False) -> dict:
    data = fetch_raw_emails(token, num_emails, unread)
    if not data:
        return []
    
    if not data.get("value"):
        return []

    emails: List[Dict[str, any]] = data["value"]
    cleaned_emails = []
    for mail in emails:
        cleaned_emails.append({
            "subject": mail["subject"],
            "from": mail["from"],
            "to_recipients": mail["toRecipients"],
            "recieved_time": mail["receivedDateTime"],
            "body": mail["body"]["content"] if mail["body"]["contentType"] != "html" else extract_text_from_html(mail["body"]["content"]),
            "is_read": mail["isRead"]
        })
    
    return cleaned_emails
    
def get_my_calendar_events(token: Token, start_date: datetime.datetime=None, end_date: datetime.datetime=None):
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