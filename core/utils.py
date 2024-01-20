import streamlit as st
import nltk
from typing import Tuple, List, Dict
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
from datetime import datetime
import base64


urgent_keywords = ["urgent", "attention", "asap", "immediate", "important", "outage"]
urgent_senders = ["boss@example.com", "hr@example.com"]  # add an email / remove


@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_page_bg_data(page: str) -> str:
    if page == "DevDynamo":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}

        [data-testid="stHeader"] {{
            background: rgba(0,0,0,0);
        }}

        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/purple1.jpg")}");
            background-position: 45% 0%; 
            background-repeat: no-repeat;
            background-attachment: local;
        }}
        </style>
        """
        # Use this to remove the empty space on top of the page
        # #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        #
        # Use this to remove "Deploy button (if header visibility is turned on"
        # .stDeployButton {{
        #         visibility: hidden;
        #     }}
        # This hids those stupid anchors ... but also removes pages from sidebar
        # /* Hide the link button https://discuss.streamlit.io/t/hide-titles-link/19783/13 */
        # .stApp a:first-child {{
        #     display: none;
        # }}
    elif page == "MailAnalyzer":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/blue2.jpg")}");
            background-repeat: no-repeat;
            background-attachment: local;
        }}
        </style>
        """
    elif page == "Calendar":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/orange1.jpg")}");
            background-repeat: no-repeat;
            background-attachment: local;
        }}
        </style>
        """
    elif page == "Todos":
        return f"""
        <style>
        header {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        #root > div:nth-child(1) > div > div > div > div > section > div {{padding-top: 0rem;}}
        [data-testid="stSidebar"] > div:first-child {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/dark_bg.jpg")}");
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: top left;
        }}
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/png;base64,{get_img_as_base64("assets/red1.jpg")}");
            background-repeat: no-repeat;
            background-attachment: local;
        }}
        </style>
        """
    return ""
    # background-position: 45% 0%; 


def initialize(page: str) -> None:
    if page == "DevDynamo":
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
        st.markdown(get_page_bg_data("DevDynamo"), unsafe_allow_html=True)
        # if "selected_text" not in st.session_state:
        #     st.session_state.selected_text = ""
        # if "search_wiki" not in st.session_state:
        #     st.session_state.search_wiki = False
    elif page == "MailAnalyzer":
        st.set_page_config(
            page_title="MailAnalyzer",
            page_icon="🔬",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("MailAnalyzer"), unsafe_allow_html=True)
    elif page == "Calendar":
        st.set_page_config(
            page_title="Calendar",
            page_icon="📅",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("Calendar"), unsafe_allow_html=True)
    elif page == "Todos":
        st.set_page_config(
            page_title="Todos",
            page_icon="📌",
            layout="wide",
            initial_sidebar_state="expanded",
        )
        st.markdown(get_page_bg_data("Todos"), unsafe_allow_html=True)


def download_nltk_packages() -> None:
    # nltk.data.path.append(os.getcwd() + "/nltk_data")
    try:
        nltk.find("corpora/wordnet.zip")
        print("Wordnet found")
    except LookupError:
        print("Wordnet not found. Downloading...")
        nltk.download("wordnet")
    #
    # try:
    #     nltk.data.find("sentiment/vader_lexicon.zip")
    #     print("Vader_lexicon found")
    # except LookupError:
    #     print("Vader_lexicon not found. Downloading...")
    #     nltk.download("vader_lexicon")
    #
    # try:
    #     nltk.data.find("corpora/stopwords.zip")
    #     print("Stopwords found")
    # except LookupError:
    #     print("Stopwords not found. Downloading...")
    #     nltk.download("stopwords")

    try:
        nltk.data.find("tokenizers/punkt")
        print("Punkt found")
    except LookupError:
        print("Punkt not found. Downloading...")
        nltk.download("punkt")

    st.session_state.check_packages_once = "MariuszPudzianowski"


def focus_email(mail_tuple: Tuple, urgent=False):
    if urgent:
        st.session_state.mail_tuple = mail_tuple
        st.session_state.mail = ""
    else:
        st.session_state.mail = mail_tuple
        st.session_state.mail_tuple = ""
    print("here")


def get_processed_tokens(text) -> List[str]:
    text = re.sub(r"[^a-zA-Z\s]", "", text).lower()

    lemmer = WordNetLemmatizer()

    cleaned_tokens = [
        lemmer.lemmatize(token)
        for token in word_tokenize(text)
    ]

    return cleaned_tokens


def is_urgent(mail_dict: Dict) -> Tuple[int, int, List[str]]:
    urgent_score = 0
    final_num_keywords = 0
    urgent_info_table = []

    # maby count how many to improve the metric
    processed_tokens = get_processed_tokens(mail_dict["subject"])
    num_keywords = 0
    for token in processed_tokens:
        if any(keyword == token for keyword in urgent_keywords):
            num_keywords += 1

    # print(num_keywords)

    if num_keywords > 0:
        # maby more than just 1
        urgent_score += 1
        final_num_keywords += num_keywords
        urgent_info_table.append("subject")


    processed_tokens = get_processed_tokens(mail_dict["body"])
    num_keywords = 0

    for token in processed_tokens:
        if any(keyword == token for keyword in urgent_keywords):
            num_keywords += 1

    if num_keywords > 1:
        urgent_score += 1
        final_num_keywords += num_keywords
        urgent_info_table.append("subject")

    if a := mail_dict["from"]["emailAddress"]["address"].lower() in urgent_senders:
        print(a)
        urgent_score += 1
        urgent_info_table.append("sender")

    # if mail_dict["recieved_time"] in urgent_senders:
        # TODO
        # processed_date = mail_dict["date"]
        # if process_time
        # if processed_date > 23 < 5:
            # urgent_score += 0.5
            # urgent_info_table.append("date")
        # pass

    return (urgent_score, final_num_keywords, urgent_info_table)


def parse_mails(mail_list: List[Dict]) -> Tuple[List[Tuple[Dict, int]], List[Dict]] :
    urgent_mails: List[Tuple[Dict, int]] = []
    non_urgent_mails: List[Dict] = []

    for mail in mail_list:
        urgency_score, _, _ = is_urgent(mail) #TODO
        if urgency_score != 0:
            urgent_mails.append((mail, urgency_score))
        else:
            non_urgent_mails.append(mail)

    return urgent_mails, non_urgent_mails


def find_overlapping_tasks(tasks):
    overlapping_tasks = []

    for i in range(len(tasks)):
        start1 = datetime.fromisoformat(tasks[i]["start_time"]["dateTime"])
        end1 = datetime.fromisoformat(tasks[i]["finish_time"]["dateTime"])

        for j in range(i + 1, len(tasks)):
            start2 = datetime.fromisoformat(tasks[j]["start_time"]["dateTime"])
            end2 = datetime.fromisoformat(tasks[j]["finish_time"]["dateTime"])

            if start1 < end2 and start2 < end1:
                overlapping_tasks.append((tasks[i], tasks[j]))

    return overlapping_tasks, len(overlapping_tasks), len(tasks)
