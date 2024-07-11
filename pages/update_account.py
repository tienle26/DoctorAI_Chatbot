import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
from connect import get_data
from page_functions import set_default_page
from crud import update_account
from PIL import Image
import os
import time

st.set_page_config(page_title="Use", page_icon="👨‍🔬", layout="wide")
navbar = st_navbar(
    ["Home", "Chat", "Search", "Appointment", "Profile", "Logout"], selected="Profile"
)

if navbar == "Logout":
    st.session_state.clear()
    st.switch_page("main.py")

elif navbar == "Profile":
    df = get_data("Account")
    user_pw = df[df["ID"] == st.session_state.ID].iloc[0]["Password"]

    placeholder = st.empty()
    with placeholder.form("Đổi mật khẩu"):
        st.markdown("### Đổi mật khẩu")
        old_pass = st.text_input(
            r"$\textsf{\normalsize Mật khẩu cũ}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        new_pass = st.text_input(
            r"$\textsf{\normalsize Mật khẩu mới}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        password = st.text_input(
            r"$\textsf{\normalsize Nhập lại mật khẩu mới}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        if password != new_pass:
            st.warning("Mật khẩu không khớp.")

        if st.form_submit_button("Xác nhận"):
            if old_pass == user_pw and password == new_pass:
                update_account(id=st.session_state.ID, password=password)
                st.success("Thay đổi mật khẩu thành công")
                time.sleep(1)
                st.switch_page("./pages/page1.py")
            else:
                st.error("Mật khẩu mới/cũ không khớp.")

else:
    set_default_page(navbar)
    st.switch_page("./pages/page1.py")

st.sidebar.header("Login")
st.sidebar.write("Chat trực tiếp với Doctor AI")
st.sidebar.header("Chat")
st.sidebar.header("Search")
st.sidebar.header("Appointment")
