import streamlit as st
from streamlit.components.v1 import html

import core.utils as utils

utils.initialize("MailAnalyzer")

st.title(":blue[MailAnalyzer]", anchor=False)

if "user_emails" not in st.session_state:
    st.warning("Login to get access to your emails")
    st.stop()

if "urgent_mails" not in st.session_state:
    st.session_state.urgent_mails = 0

if "mail_tuple" not in st.session_state:
    st.session_state.mail_tuple = ""

if "mail" not in st.session_state:
    st.session_state.mail = ""

with st.sidebar:
    st.info("You can click on any of your emails to get more informaction about them")

font = "Georgia"

urgent_mails, non_urgent_mails = utils.parse_mails(st.session_state.user_emails)

st.session_state.urgent_mails = len(urgent_mails)

mails_sorted = sorted(urgent_mails, key=lambda x: x[1], reverse=True)

task_list_helper = st.session_state.task_list_helper

# with st.container(border=True):
    # st.metric(label="Urgent mails", value=st.session_state.urgent_mails)
with st.container(border=True):
    st.metric(label="Urgent emails", value=st.session_state.urgent_mails, delta=f"out of {st.session_state.current_num_emails}")

st.write("\n")


with st.container(border=True):
    st.markdown( f"""
    <div style="font-size: larger; font-weight: bold; font-family: {font};color: orange;">
    Urgent mails sorted by urgency
    </div>
    """, unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")

    if mails_sorted:

        for i, mail_tuple in enumerate(mails_sorted):
            with st.container(border=True):
                mail, urgency_score = mail_tuple

                title = mail["subject"] + " - " + mail["from"]["emailAddress"]["address"]

                if len(title) > 200:
                    title = title[:200] + "..."

                st.button(
                        title,
                        key="urgent_" + str(i),
                        on_click=utils.focus_email,
                        args=(mail_tuple, True),
                    )
                st.write(f"Urgency score: {urgency_score}/5")

    else:
        st.markdown( f"""
        <div style="font-size: medium; font-weight: bold; font-family: {font};">
        No urgent mails
        </div>
        """, unsafe_allow_html=True)


with st.container(border=True):
    st.markdown( f"""
    <div style="font-size: larger; font-weight: bold; font-family: {font}; color: green;">
    Non-urgent emails
    </div>
    """, unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")

    if non_urgent_mails:
        for i, mail in enumerate(non_urgent_mails, 1):
            title = mail["subject"] + " - " + mail["from"]["emailAddress"]["address"]

            if len(title) > 200:
                title = title[:200] + "..."

            st.button(
                    title,
                    key="non_urgent_" + str(i),
                    on_click=utils.focus_email,
                    args=(mail, False),
                )
    else:
        st.markdown( f"""
        <div style="font-size: medium; font-weight: bold; font-family: {font};">
        No non-urgent emails
        </div>
        """, unsafe_allow_html=True)


if st.session_state.mail_tuple:
    mail_tuple = st.session_state.mail_tuple
    with st.chat_message(name="human", avatar="📜"):
        st.write(f"Subject: {mail_tuple[0]['subject']}")
        st.write("From:")
        st.write(f" - {mail_tuple[0]['from']['emailAddress']['name']}")
        st.write(f" - {mail_tuple[0]['from']['emailAddress']['address']}")
        st.write(f"Date: {mail_tuple[0]['recieved_time'][:10]}")
        st.write(f"Time: {mail_tuple[0]['recieved_time'][11:16]}")
        st.write(f"Content:")
        html(mail_tuple[0]['html_body'], height=300, scrolling=True)


    if st.button(
            "Create a TODO",
            # key="urgent_" + str(i),
            # on_click=utils.focus_email,
            # args=(mail_tuple, True),
            ):
        with st.form("email_form"):
            task_bucket = st.selectbox("Task bucket", [l["name"] for l in st.session_state.task_list_helper])
            title = st.text_input("Title", value=mail_tuple[0]['subject'])
            description = st.text_input("Description")
            d = st.date_input("When's your birthday")
            importance = st.selectbox("Importance", ["normal", "high"])

            submitted = st.form_submit_button("Create a TODO")

        if submitted:
            create_new_todo(st.session_state.auth_token, )
            

if st.session_state.mail:
    mail = st.session_state.mail
    with st.chat_message(name="human", avatar="📜"):
        st.write(f"Subject: {mail['subject']}")
        st.write("From:")
        st.write(f" - {mail['from']['emailAddress']['name']}")
        st.write(f" - {mail['from']['emailAddress']['address']}")
        st.write(f"Date: {mail['recieved_time'][:10]}")
        st.write(f"Time: {mail['recieved_time'][11:16]}")
        st.write(f"Content:")
        html(mail['html_body'], height=300, scrolling=True)
