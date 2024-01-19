import streamlit as st
import requests
from urllib.parse import urlencode
from config import Config
import datetime
from ms_conn.classes import Token
from pprint import pprint
config = Config.from_toml("config.toml")

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
    
def get_my_calendar_events(token: Token, start_date: datetime.datetime=None, end_date: datetime.datetime=None):
    headers = {
        'Authorization': f'Bearer {token.access_token}',
        'Content-Type': 'application/json'
    }

    # If no dates are specified, fetch events for the current day
    if not start_date:
        start_date = datetime.datetime.utcnow().date()
    if not end_date:
        end_date = start_date + datetime.timedelta(weeks=2)

    # Convert dates to the correct format (ISO 8601)
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

def main():
    # Streamlit UI
    st.title("Microsoft Calendar Events")

    if 'auth_token' not in st.session_state:
            # Generate the Microsoft login URL
            auth_link = generate_auth_url()
            st.markdown(f'[Login with Microsoft]({auth_link})')

            # Check if the authorization code is in the URL
            auth_code = st.query_params.get("code")

            if auth_code:
                token = exchange_code_for_token(auth_code)
                token = Token.from_dict(token)
                if token:
                    st.session_state['auth_token'] = token
                    st.success('Logged in successfully.')
                else:
                    st.error('Failed to retrieve the token.')

    if 'auth_token' in st.session_state:
        token: Token = st.session_state["auth_token"]
        # Adding a number input for the number of emails to fetch
        num_emails = st.number_input('Number of emails to fetch', min_value=1, max_value=100, value=10)

            # Adding a checkbox for fetching only unread emails
        unread = st.checkbox('Fetch only unread emails')

        if st.button('Fetch Emails'):
            user_emails = get_user_emails(token=token, num_emails=num_emails, unread=unread)

            # Check if the response is successful
            if isinstance(user_emails, dict):
                emails = user_emails.get('value', [])
                for email in emails:
                    st.write(f"Subject: {email['subject']}")
            else:
                st.error(user_emails)

        if st.button('Fetch Events'):
            my_events = get_my_calendar_events(token)

            if isinstance(my_events, dict):
                events = my_events.get('value', [])
                for event in events:
                    pprint(event)
                    st.write(f"Event: {event['subject']} on {event['start']['dateTime']}")
            else:
                st.error(my_events)