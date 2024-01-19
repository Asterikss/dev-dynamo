import streamlit as st

import core.utils as utils

utils.initialize("DevDynamo")

st.title(":green[DevDynamo]", anchor=False)
st.header("Homepage", anchor=False)

c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.metric(label="Conflicting meetings", value=0, delta=-1)
with c2:
    with st.container(border=True):
        st.metric(label="Screen time", value="25h", delta=+2)
with c3:
    with st.container(border=True):
        st.metric(label="Urgent mails", value=1, delta=-1)
