import streamlit as st
from . import *
import webbrowser


def main(num_emails: int, unread: bool):
    if "auth_token" not in st.session_state:
        auth_code = st.query_params.get("code")

        # Check if the authorization code is in the URL
        if auth_code:
            token = exchange_code_for_token(auth_code)
            print(token)
            token = Token.from_dict(token)
            if token:
                st.session_state["auth_token"] = token
            else:
                st.error("Failed to retrieve the token.")
                st.query_params.pop("code")

        else:
            if st.button("Login with Microsoft"):
                webbrowser.open(generate_auth_url(), new=0)

            st.write("\n")

    if "auth_token" in st.session_state:
        token: Token = st.session_state["auth_token"]

        if st.button("Fetch Emails and Events"):
            st.session_state.user_emails = get_user_emails(
                token=token, num_emails=num_emails, unread=unread
            )
            st.session_state.user_events = get_my_calendar_events(token)
            st.session_state.current_num_emails = num_emails
            st.session_state.tasks_lists = get_tasks_in_lists(token)
            st.session_state.task_list_helper = get_task_lists(token)
