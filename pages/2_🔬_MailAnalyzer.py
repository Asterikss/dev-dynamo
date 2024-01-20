import streamlit as st

import core.utils as utils


st.title(":blue[MailAnalyzer]", anchor=False)

if "user_emails" not in st.session_state:
    st.warning("Log in to get access to your emails")
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

with st.container(border=True):
    st.metric(label="Urgent mails", value=st.session_state.urgent_mails)

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
        st.write(mail_tuple[0]['body'])


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
        st.write(mail['body'])
