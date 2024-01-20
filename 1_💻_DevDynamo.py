import streamlit as st

import core.utils as utils
from ms_conn.ms_conn import main as ms_main

utils.initialize("DevDynamo")

if "check_packages_once" not in st.session_state:
    utils.download_nltk_packages()

st.title(":green[DevDynamo]", anchor=False)

with st.sidebar:
    num_emails = st.slider("How many emails to fetch", 0, 20, 2)
    unread = st.checkbox('Fetch only unread emails')

ms_main(num_emails, unread)

st.write("\n")
st.write("\n")

st.header("Dashboard", anchor=False)

if "user_emails" not in st.session_state:
    st.warning("Log in to get access to your Dashboard")
    st.stop()

urgent_mails, non_urgent_mails = utils.parse_mails(st.session_state.user_emails)

_, n_overlapping_tasks, n_tasks = utils.find_overlapping_tasks(st.session_state.user_events)


st.session_state.urgent_mails = len(urgent_mails)

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.metric(label="Urgent emails", value=st.session_state.urgent_mails, delta=f"out of {st.session_state.current_num_emails}")
with c2:
    with st.container(border=True):
        st.metric(label="Conflicting events", value=n_overlapping_tasks, delta=f"out of {n_tasks}")
with c3:
    with st.container(border=True):
        st.metric(label="Screen time", value="25h", delta=+2)
