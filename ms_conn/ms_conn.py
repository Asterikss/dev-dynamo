import streamlit as st
from . import *

def main(num_emails: int, unread: bool):

    if 'auth_token' not in st.session_state:
            auth_code = st.query_params.get("code")

            if auth_code:
                token = exchange_code_for_token(auth_code)
                token = Token.from_dict(token)
                if token:
                    st.session_state['auth_token'] = token
                else:
                    st.error('Failed to retrieve the token.')
            else: 
                with st.container(border=True):
                    st.markdown( f"""
                    <div style="font-size: larger; font-weight: bold; font-family: Georgia;color: orange;">
                    <a href="{generate_auth_url()}" target="_self">Login with Microsoft</a>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("\n")


            # Check if the authorization code is in the URL


    if 'auth_token' in st.session_state:
        token: Token = st.session_state["auth_token"]

        if st.button("Fetch Emails and Events"):
            st.session_state.user_emails = get_user_emails(token=token, num_emails=num_emails, unread=unread)
            st.session_state.user_events = get_my_calendar_events(token)
            st.session_state.current_num_emails = num_emails
