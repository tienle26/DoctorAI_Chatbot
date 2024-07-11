import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
from connect import get_data, create_credentials
from page_functions import home, search_drugs, appointment, profile
from crud import filter_appointment, cancel_appointment
from chat import chatbot

create_credentials()
st.set_page_config(page_title="Use", page_icon="👨‍🔬", layout="wide")
navbar = st_navbar(
    ["Home", "Chat", "Search", "Appointment", "Profile", "Logout"],
    selected=st.session_state.default_page,
)

if navbar == "Home":
    home()

elif navbar == "Chat":
    chatbot()

elif navbar == "Search":
    search_drugs()

elif navbar == "Appointment":
    appointment()

elif navbar == "Logout":
    st.session_state.clear()
    st.switch_page("main.py")

elif navbar == "Profile":
    profile()

st.sidebar.header("Login")
st.sidebar.write("Chat trực tiếp với Doctor AI")
st.sidebar.header("Chat")
st.sidebar.header("Search")
st.sidebar.header("Appointment")
