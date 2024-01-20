import streamlit as st
from datetime import datetime, timezone, date
import core.utils as utils
import pytz

def convert_to_warsaw_date(datetime_str):
    truncated_datetime_str = datetime_str[:26]

    utc_datetime = datetime.strptime(truncated_datetime_str, '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc)

    warsaw_tz = pytz.timezone('Europe/Warsaw')

    warsaw_date = utc_datetime.astimezone(warsaw_tz).date()

    return warsaw_date

def prepare_todo(todo: dict) -> int:
    imp = 0
    if todo["importance"] == "low":
        imp = 1
    elif todo["importance"] == "normal":
        imp = 2
    else:
        imp = 3
    
    if todo['due_date_time']:
        days = (convert_to_warsaw_date(todo['due_date_time']['dateTime']) - date.today()).days
        return days / imp
    
    return 31 / imp
    
        

utils.initialize("Todos")

st.title(":red[Todos]", anchor=False)

if "user_emails" not in st.session_state:
    st.warning("Login to get access to your Calendar")
    st.stop()

todo_list = st.session_state.tasks_lists

n_todos = sum(len(todos) for todos in todo_list.values())
n_todos_high = sum(1 for todos in todo_list.values() for todo in todos if todo["importance"] == "high")

with st.container(border=True):
    st.metric(label="Todos", value=n_todos, delta=f"{n_todos_high} of high importance")

with st.container(border=True):
    todo_lists = {list_name: todos for (list_name, todos) in todo_list.items() if todos}

    for list_name, todos in todo_lists.items():
        sorted_todos = sorted(todos, key=lambda todo: prepare_todo(todo))
        st.subheader(f"{list_name}:", anchor=False)
        st.markdown(
            """<hr style="height:5px;width:70%;border:none;color:#333;background-color:#333; margin-top:0; margin-bottom:0;" /> """,
            unsafe_allow_html=True,
        )
        print(sorted_todos)
        print([prepare_todo(todo) for todo in sorted_todos])
        for todo in sorted_todos:
            with st.container(border=True):
                st.write(f"Title: {todo['title']}")
                st.write(f"Importance: {todo['importance']}")
                if todo['due_date_time']:
                    st.write(f"Due to: {convert_to_warsaw_date(todo['due_date_time']['dateTime'])}")




