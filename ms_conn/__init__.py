from typing import Dict, List
import streamlit as st
import requests
from urllib.parse import urlencode
from config import config
import datetime
from .classes import Token
from .fetch_funcs import fetch_raw_emails, fetch_raw_calendart_events
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

def get_user_emails(token: Token, num_emails: int = 10, unread: bool = False) -> List[Dict[str, any]]:
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
    
def get_my_calendar_events(token: Token, start_date: datetime.datetime=None, end_date: datetime.datetime=None) -> List[Dict[str, any]]:
    data = fetch_raw_calendart_events(token, start_date, end_date)
    if not data:
        return []
    
    if not data.get("value"):
        return []
    
    events: List[Dict[str, any]] = data["value"]
    cleaned_events = []
    pprint(events)
    for event in events:
        cleaned_events.append(event)
    
    return cleaned_events
    