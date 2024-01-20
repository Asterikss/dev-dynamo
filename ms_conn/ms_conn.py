import streamlit as st
from . import *

def main():
    # Streamlit UI
    st.title("Microsoft Calendar Events")

    if 'auth_token' not in st.session_state:
            # Generate the Microsoft login URL
            auth_link = generate_auth_url()
            st.markdown(f'<a href="{auth_link}" target="_self">Login with Microsoft</a>', unsafe_allow_html=True)

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

        
            for email in user_emails:
                st.write(f"Subject: {email['subject']}")
        
        if st.button('Fetch Events'):
            my_events = get_my_calendar_events(token)

            for event in my_events:
                st.write(f"Event: {event['subject']} on {event['start']['dateTime']}")
            else:
                st.error(my_events)