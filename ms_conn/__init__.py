from typing import Dict, List
import streamlit as st
import requests
from urllib.parse import urlencode
from config import config
import datetime
from .classes import Token
from .fetch_funcs import fetch_raw_emails, fetch_raw_calendart_events, fetch_task_lists, fetch_tasks_in_list
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
            "html_body": mail["body"]["content"],
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
    for event in events:
        cleaned_events.append({
            "start_time": event["start"],
            "finish_time": event["end"],
            "title": event["subject"],
            "is_cancelled": event["isCancelled"],
            "is_all_day": event["isAllDay"],
            "organizer": event["organizer"]
        })
    
    return cleaned_events
    
def get_task_lists(token: Token):
    data = fetch_task_lists(token)
    if not data:
        return []
    
    if not data.get("value"):
        return []
    
    task_lists: List[Dict[str, any]] = data["value"]
    cleaned_lists = [
        {
            "name": l["displayName"],
            "id": l["id"]
        } for l in task_lists]
    return cleaned_lists
    
    
def get_tasks_in_list(token: Token, list_id: str):
    data = fetch_tasks_in_list(token=token, list_id=list_id)
    if not data:
        return []
    
    if not data.get("value"):
        return []
    
    tasks: List[Dict[str, any]] = data["value"]
    return [{
        "title": task["title"],
        "importance": task["importance"],
        "due_date_time": task["dueDateTime"]
    } for task in tasks]

def get_tasks_in_lists(token: Token):
    task_lists = get_task_lists(token)
    result = {}
    for task_list in task_lists:
        result[task_list["name"]] = get_tasks_in_list(token, task_list["id"])

def create_new_todo(token: Token, task_list_id: str, task_title: str, details: str=None, due_date: str=None):
    url = f"https://graph.microsoft.com/v1.0/me/todo/lists/{task_list_id}/tasks"
    headers = {
        "Authorization": f"Bearer {token.access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "title": task_title,
        "body": {
            "contentType": "text",
            "content": details if details else ""
        }
    }
    if due_date:
        data["dueDateTime"] = {
            "dateTime": due_date.isoformat(),
            "timeZone": "UTC"
        }
    response = requests.post(url, headers=headers, json=data)
    return response.json()