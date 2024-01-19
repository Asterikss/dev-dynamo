import streamlit as st

def initialize(page: str) -> None:
    if page == "Analyzer":
        st.set_page_config(
            page_title="DevDynamo",
            page_icon="💻",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                'Get Help': 'https://www.extremelycoolapp.com/help',
                'Report a bug': "https://www.extremelycoolapp.com/bug",
                'About': "# This is a header. This is an *extremely* cool app!"
            }
        )
        # st.markdown(get_page_bg_data("DevDynamo"), unsafe_allow_html=True)
        if "selected_text" not in st.session_state:
            st.session_state.selected_text = ""
        if "search_wiki" not in st.session_state:
            st.session_state.search_wiki = False
    elif page == "DataExplorer":
        st.set_page_config(
            page_title="MailAnalyzer",
            page_icon="🔬",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        # st.markdown(get_page_bg_data("MailAnalyzer"), unsafe_allow_html=True)
