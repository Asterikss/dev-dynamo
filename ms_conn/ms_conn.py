import streamlit as st
from . import *

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