import streamlit as st

import core.utils as utils

utils.initialize("Calendar")

st.title(":orange[Calendar]", anchor=False)

if "user_emails" not in st.session_state:
    st.warning("Login to get access to your Calendar")
    st.stop()

events = st.session_state.user_events

overlapping_tasks, n_overlapping_tasks, n_tasks = utils.find_overlapping_tasks(st.session_state.user_events)

with st.container(border=True):
    st.metric(label="Conflicting events", value=n_overlapping_tasks, delta=f"out of {n_tasks}")


if n_overlapping_tasks > 0:
    with st.container(border=True):
        st.markdown( f"""
        <div style="font-size: larger; font-weight: bold; font-family: Georgia ;color: orange;">
        Overlapping events
        </div>
        """, unsafe_allow_html=True)

        st.write("\n")
        st.write("\n")

        over_c1, over_c2 = st.columns(2)

        for event1, event2 in overlapping_tasks:

            with over_c1:
                with st.container(border=True):
                    st.write(f"Title: {event1['title']}")
                    st.write(f"Date: {event1['start_time']['dateTime'][:10]}")
                    st.write(f"Start: {event1['start_time']['dateTime'][11:16]}")
                    st.write(f"End: {event1['finish_time']['dateTime'][11:16]}")

            with over_c2:
                with st.container(border=True):
                    st.write(f"Title: {event2['title']}")
                    st.write(f"Date: {event2['start_time']['dateTime'][:10]}")
                    st.write(f"Start: {event2['start_time']['dateTime'][11:16]}")
                    st.write(f"End: {event2['finish_time']['dateTime'][11:16]}")


with st.container(border=True):
    st.markdown( f"""
    <div style="font-size: larger; font-weight: bold; font-family: Georgia ;color: green;">
    All events
    </div>
    """, unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")

    c1, c2, c3 = st.columns(3)

    for i, event in enumerate(events):
        index = i%3

        if index == 0:
            with c1:
                with st.container(border=True):
                    st.write(f"Title: {event['title']}")
                    st.write(f"Date: {event['start_time']['dateTime'][:10]}")
                    st.write(f"Start: {event['start_time']['dateTime'][11:16]}")
                    st.write(f"End: {event['finish_time']['dateTime'][11:16]}")
        elif index == 1:
            with c2:
                with st.container(border=True):
                    st.write(f"Title: {event['title']}")
                    st.write(f"Date: {event['start_time']['dateTime'][:10]}")
                    st.write(f"Start: {event['start_time']['dateTime'][11:16]}")
                    st.write(f"End: {event['finish_time']['dateTime'][11:16]}")
        elif index == 2:
            with c3:
                with st.container(border=True):
                    st.write(f"Title: {event['title']}")
                    st.write(f"Date: {event['start_time']['dateTime'][:10]}")
                    st.write(f"Start: {event['start_time']['dateTime'][11:16]}")
                    st.write(f"End: {event['finish_time']['dateTime'][11:16]}")

