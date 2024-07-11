import streamlit as st
from streamlit_navigation_bar import st_navbar
from connect import create_credentials
from page_functions import (
    home,
    search_drugs,
    login,
    set_sessionID,
    set_default_page,
)

create_credentials()
set_default_page()
st.set_page_config(page_title="Use", page_icon="👨‍🔬", layout="wide")
navbar = st_navbar(["Home", "Chat", "Search", "Appointment", "Login"])
set_sessionID()

if navbar == "Home":
    home()

elif navbar == "Chat":
    st.warning("Please login to chat")

elif navbar == "Search":
    search_drugs()

elif navbar == "Appointment":
    st.warning("Please login to book an appointment")

elif navbar == "Login":
    login()

st.sidebar.header("Login")
st.sidebar.write("Chat trực tiếp với Doctor AI")
st.sidebar.header("Chat")
st.sidebar.header("Search")
st.sidebar.header("Appointment")
