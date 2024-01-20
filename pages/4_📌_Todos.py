import streamlit as st

st.title(":violet[Todos]", anchor=False)

if "user_emails" not in st.session_state:
    st.warning("Log in to get access to your Calendar")
    st.stop()

todo_list = st.session_state.tasks_lists

n_todos = sum(len(todos) for todos in todo_list.values())
n_todos_high = sum(1 for todos in todo_list.values() for todo in todos if todo["importance"] == "high")

with st.container(border=True):
    st.metric(label="Todos", value=n_todos, delta=f"{n_todos_high} of high importance")

st.write(todo_list)

with st.container(border=True):
    for todo_topic in todo_list.keys():
        if todo_list[todo_topic]:
            with st.container(border=True):
                st.write(f"{todo_topic}:")
                st.markdown(
                        """<hr style="height:5px;width:70%;border:none;color:#333;background-color:#333; margin-top:0; margin-bottom:0;" /> """,
                        unsafe_allow_html=True,
                    )
                with st.container(border=True):
                    st.write(f"Title: {todo_list[todo_topic][0]['title']}")
                    st.write(f"Importance: {todo_list[todo_topic][0]['importance']}")
                    st.write(f"Due to: {todo_list[todo_topic][0]['due_date_time']}")




