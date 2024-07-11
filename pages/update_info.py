import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
from connect import get_data
from page_functions import set_default_page
from crud import update_patient_record
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
    placeholder = st.empty()
    with placeholder.form("Chỉnh sửa thông tin cá nhân"):
        name = st.text_input(
            r"$\textsf{\normalsize Tên}$:red[$\textsf{\normalsize *}$]", type="default"
        )
        age = st.text_input(
            r"$\textsf{\normalsize Tuôi}$:red[$\textsf{\normalsize *}$]", type="default"
        )
        phone = st.text_input(
            r"$\textsf{\normalsize Số điện thoại}$:red[$\textsf{\normalsize *}$]",
            type="default",
        )
        gender = st.radio("Gender", ("Male", "Female", "Prefer Not To Say"))

        uploaded_file = st.file_uploader("Chọn ảnh", type=["jpg", "jpeg", "png"])
        if uploaded_file == None:
            image = ""
        else:
            saved_image = Image.open(uploaded_file)
            # Save the image using PIL
            image_path = f"{st.session_state.ID}.png"
            if os.path.exists(image_path):
                os.remove(image_path)

            saved_image.save(image_path)
            image = image_path

        if st.form_submit_button("Xác nhận"):
            update_patient_record(
                id=st.session_state.ID,
                name=name,
                age=age,
                phone=phone,
                gender=gender,
                image=image,
            )
            st.success("Thay đổi thông tin thành công")
            time.sleep(1)
            st.switch_page("./pages/page1.py")
else:
    set_default_page(navbar)
    st.switch_page("./pages/page1.py")

st.sidebar.header("Login")
st.sidebar.write("Chat trực tiếp với Doctor AI")
st.sidebar.header("Chat")
st.sidebar.header("Search")
st.sidebar.header("Appointment")
