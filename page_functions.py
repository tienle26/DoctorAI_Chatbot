import streamlit as st
from streamlit_navigation_bar import st_navbar
import bcrypt
import time
import datetime
import random
import string
from connect import get_data
from crud import (
    create_patient_record,
    create_account,
    create_appointment,
    update_appointment,
    cancel_appointment,
    filter_appointment,
    is_existed,
    find_accountID,
    get_password,
)


def set_sessionID() -> None:
    if "ID" not in st.session_state:
        st.session_state.ID = None


def set_default_page(page="Home") -> None:
    if "default_page" not in st.session_state:
        st.session_state.default_page = page
    else:
        st.session_state.default_page = page


def home() -> None:
    st.header("Doctor AI - Trợ Lý Sức Khỏe Cá Nhân Của Bạn")
    st.image("Image/chatbot.jpg", output_format="auto")
    st.write(
        "Mô Tả: Đưa sức khỏe của bạn vào tay của công nghệ với Doctor AI - chatbot y tế tiên tiến nhất, hỗ trợ bạn từ việc chẩn đoán ban đầu đến quản lý bệnh mãn tính."
    )
    st.header("Doctor AI là gì?")
    st.write(
        "Doctor AI là một chatbot y tế thông minh, được thiết kế để cung cấp cho bạn các lời khuyên y tế chính xác và kịp thời. Với sự hỗ trợ của công nghệ AI tiên tiến, Doctor AI có khả năng chẩn đoán các triệu chứng ban đầu, cung cấp thông tin về các bệnh lý và giúp quản lý các bệnh mãn tính."
    )
    st.header("Những Tính Năng Nổi Bật của Doctor AI")
    st.write(
        "+ Chẩn Đoán Ban Đầu: Phân tích các triệu chứng và đưa ra các dự đoán về bệnh lý có thể mắc phải."
    )
    st.write(
        "+ Thông Tin Y Khoa Đầy Đủ: Cung cấp thông tin chi tiết về các bệnh lý, thuốc và phương pháp điều trị."
    )
    st.header("Doctor AI Hoạt Động Như Thế Nào?")
    st.write(
        "Doctor AI sử dụng công nghệ AI tiên tiến để phân tích dữ liệu y tế từ người dùng. Bạn chỉ cần nhập các triệu chứng hoặc câu hỏi của mình, Doctor AI sẽ phân tích và cung cấp câu trả lời chính xác nhất."
    )
    st.header("Contact")
    st.image("Image/chusoc.jpg", width=200)
    st.write("Bác sĩ online")
    st.write("Email: lapduanviet@gmail.com")
    st.write("Phone: 0918755356")


def register() -> None:
    # form dang ky
    placeholder = st.empty()
    with placeholder.form("Chưa có tài khoản"):
        st.markdown("### Đăng ký")
        email2 = st.text_input("Email")
        characters = string.ascii_letters + string.digits
        id = "".join(random.choice(characters) for i in range(8))
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

        new_pass = st.text_input(
            r"$\textsf{\normalsize Mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        password = st.text_input(
            r"$\textsf{\normalsize Nhập lại mật khẩu}$:red[$\textsf{\normalsize *}$]",
            type="password",
        )

        if password != new_pass:
            st.warning("Mật khẩu không khớp.")

        # button submit
        submit = st.form_submit_button("Đăng ký")
        if submit:
            if not is_existed(email2) and "@gmail.com" in email2:
                time.sleep(0.5)
                create_account(id, email2, password)
                create_patient_record(id, email2, name, age, phone, gender)

                st.session_state.ID = id
                st.success("Đăng ký thành công")
                st.switch_page("./pages/page1.py")

            else:
                st.warning("Email không hợp lệ")


def login() -> None:
    # form login
    placeholder = st.empty()
    with placeholder.form("login"):
        st.markdown("### Đăng nhập")
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        # button submit
        submit = st.form_submit_button("Đăng nhập")

    # check status
    if password != "" or email != "":
        # check account
        actual_pass = get_password(email)
        print("actual_pass:", actual_pass)

        if actual_pass != 0:
            # encode password
            if bcrypt.checkpw(password.encode(), actual_pass):
                st.success("Đăng nhập thành công")
                user_id = find_accountID(email)
                # print(user_id)
                # update_historylogs(user_id, email, str(time.localtime()))
                # placeholder = st.empty()
                time.sleep(0.5)

                st.session_state.ID = user_id
                st.switch_page("./pages/page1.py")
            else:
                st.warning("Password/Email không hợp lệ")

        else:
            st.warning("Password/Email không hợp lệ")

    register()


def search_drugs() -> None:
    def find_drug(df, text_search):
        # Filter the dataframe using masks
        if text_search:
            m1 = df["Name"].str.contains(text_search, case=False)
            m2 = df["Brand"].str.contains(text_search, case=False)
            df_search = df[m1 | m2]
            return df_search
        return pd.DataFrame()

    st.markdown(
        "<h1 style='text-align: center; color: black;'>Công Cụ Tìm Kiếm Thuốc</h1>",
        unsafe_allow_html=True,
    )

    # Connect to the drug dataset
    df = get_data("Drug")

    # Use a text_input to get the keywords to filter the dataframe
    text_search = st.text_input(
        "Nhập tên thuốc, thương hiệu thuốc hoặc tên bệnh", value=None
    )

    # Show the cards
    N_cards_per_row = 3
    if text_search:
        df_search = find_drug(df, text_search)

        if df_search.empty:
            st.markdown(
                "<h1 style='text-align: center; color: black; font-size: 20px;'>Không tìm thấy sản phẩm phù hợp.</h1>",
                unsafe_allow_html=True,
            )

        for n_row, row in df_search.reset_index().iterrows():
            i = n_row % N_cards_per_row
            if i == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")

            # draw the card
            with cols[n_row % N_cards_per_row]:
                name = row["Name"].strip()
                brand = row["Brand"].strip()
                img_link = row["Image Link"].strip()
                drug_link = row["Link"].strip()

                st.image(img_link, use_column_width=True)
                st.write(f"[{name}]({drug_link})")

                if row["Price"] != "['None']":
                    f = "'"
                    price = row["Price"][1:-1].replace(f, "").strip()
                    st.markdown(f"Giá: {price}")


def appointment() -> None:
    def select_name(name):
        st.session_state["selected_name"] = name

    def select_time(slot):
        st.session_state["selected_time"] = slot

    def select_day(day):
        st.session_state["selected_day"] = day

    st.markdown(
        "<h1 style='text-align: center; color: black;'>Đặt Lịch Hẹn Bác Sĩ</h1>",
        unsafe_allow_html=True,
    )

    df = get_data("Doctor")

    availability = df["Availability"]
    time_slots = df["TimeSlots"]

    if "selected_time" not in st.session_state:
        st.session_state["selected_time"] = None

    doctor_columns, booking_column = st.columns([4, 3])

    # Doctors' individual information
    with doctor_columns:
        st.header("Thông Tin Bác Sĩ")
        temp_col_1, temp_col_2 = st.columns([1, 1])
        with temp_col_1:
            doctor_name = st.selectbox(
                r"$\textsf{\normalsize Chọn bác sĩ}$:red[$\textsf{\normalsize *}$]",
                df["Name"].to_list(),
            )
            select_name(doctor_name)
        doctor_info = df[df["Name"] == doctor_name]

        col_1, col_2 = st.columns([1, 1])
        with col_1:
            if doctor_info["Image"].values[0] != "None":
                st.image(doctor_info["Image"].values[0], width=250)
            else:
                unknown_doctor = "Image/Unknown_person.jpg"
                st.image(unknown_doctor, width=250)
        with col_2:
            st.subheader(doctor_name)
            st.write(f"*{doctor_info['Title'].values[0]}*")
            st.write(f"*Chuyên Ngành:* {doctor_info['Speciality'].values[0]}")

        # Inject custom CSS for the buttons
        st.markdown(
            """
            <style>
            div.stButton > button {
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Days
        st.write(f"*Ngày Khám Trong Tuần:*")
        col = st.columns([1, 1, 1, 1, 1])
        available_days = doctor_info["Availability"].values[0].split(", ")
        unavailable_days = []

        for idx in range(len(available_days)):
            col_idx = idx if idx < 4 else idx - 4
            with col[col_idx]:
                # st.button(available_days[idx])
                if available_days[idx] in unavailable_days:
                    st.button(
                        available_days[idx], disabled=True, key=available_days[idx]
                    )
                else:
                    if st.button(available_days[idx], key=available_days[idx]):
                        select_time(available_days[idx])

        # Available slot
        st.write("*Thời gian khám:*")
        unavailable_slots = []
        available_slots = doctor_info["TimeSlots"].values[0].split(",")
        N_cards_per_row = 4

        for idx in range(len(available_slots)):
            i = idx % N_cards_per_row
            if i == 0:
                cols = st.columns(N_cards_per_row * 2 - 1, gap="small")
            # draw the card
            with cols[idx % N_cards_per_row]:
                if available_slots[idx] in unavailable_slots:
                    st.button(
                        available_slots[idx], key=available_slots[idx], disabled=True
                    )
                else:
                    if st.button(available_slots[idx], key=available_slots[idx]):
                        select_time(available_slots[idx])

    with booking_column:
        st.header("Thông Tin Lịch Hẹn")
        doctor_name = st.session_state["selected_name"]
        date = st.date_input(
            r"$\textsf{\normalsize Chọn ngày khám}$:red[$\textsf{\normalsize *}$]",
            min_value=datetime.date.today(),
        )

        # Determine available slots by excluding unavailable ones
        doctor_info = df[df["Name"] == doctor_name]
        unavailable_slots = []

        all_slots = doctor_info["TimeSlots"].values[0].split(",")
        available_slots = [slot for slot in all_slots if slot not in unavailable_slots]

        # Maintain consistency with unavailable slots and session state
        selected_time = st.selectbox(
            r"$\textsf{\normalsize Thời gian khám}$:red[$\textsf{\normalsize *}$]",
            available_slots,
            index=(
                available_slots.index(st.session_state["selected_time"])
                if st.session_state["selected_time"] in available_slots
                else 0
            ),
        )
        symptoms = st.text_area(
            r"$\textsf{\normalsize Triệu chứng}$",
            placeholder="Nhập triệu chứng của bạn",
            height=300,
        )
        notes = st.text_area(
            r"$\textsf{\normalsize  Ghi chú}$",
            placeholder="Ghi chú thêm dành cho bác sĩ",
            height=200,
        )

        # Button to book appointment
        if st.button("Đặt hẹn"):
            characters = string.ascii_letters + string.digits
            ID = "".join(random.choice(characters) for i in range(8))
            PatientID = st.session_state.ID
            DoctorID = doctor_info.iloc[0]["ID"]
            Time = str(date) + " " + selected_time
            Description = f"Triệu chứng: {symptoms}. Ghi chú: {notes}"

            create_appointment(ID, PatientID, DoctorID, Time, Description)

            st.success(
                f"Đặt lịch hẹn thành công với {doctor_name}."
                f" Thời gian {date.strftime('%A, %B %d, %Y')} vào lúc {selected_time}"
            )


def profile() -> None:
    if st.session_state.ID != None:
        df = get_data("Patient")
        user_df = df[df["ID"] == st.session_state.ID].iloc[0]

        Name = user_df["Name"]
        Age = user_df["Age"]
        Email = user_df["Email"]
        Phone = user_df["Phone"]
        Image = user_df["Image"]

        ################ Profile ################
        st.title("Thông tin cá nhân")
        col1, col2 = st.columns(2)

        with col1:
            if Image == "":
                st.image("Image/Unknown_person.jpg", width=250)
            else:
                st.image(Image, width=250)
        with col2:
            st.write(f"📝  Tên: {Name}")
            st.write(f"📜  Tuổi: {Age}")
            st.write(f"📧  Email: {Email}")
            st.write(f"📞  SDT: {Phone}")

            col3, col4, col5 = st.columns(3)
            with col3:
                change_info = st.button("Cập nhật")
                if change_info:
                    st.switch_page("./pages/update_info.py")

            with col4:
                change_acc = st.button("Đổi mật khẩu")
                if change_acc:
                    st.switch_page("./pages/update_account.py")

        ################# Appointment #################
        st.header("Lịch hẹn sắp tới 📥")
        appointment = filter_appointment(st.session_state.ID)

        if not appointment.empty:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 2, 3, 1, 1])

            # write Header
            col1.write("ID")
            col2.write("DoctorID")
            col3.write("Time")
            col4.write("Description")
            st.write("___" * 20)

            # write contents
            col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 2, 3, 1, 1])
            # Custom CSS to adjust spacing between elements
            st.markdown(
                """
                <style>
                .custom-row-space {
                    margin-bottom: 30px; /* Adjust this value to increase/decrease space */
                }
                </style>
            """,
                unsafe_allow_html=True,
            )

            for i, row in appointment.iterrows():
                col1.markdown(
                    f'<div class="custom-row-space">{row["ID"]}</div>',
                    unsafe_allow_html=True,
                )
                col2.markdown(
                    f'<div class="custom-row-space">{row["DoctorID"]}</div>',
                    unsafe_allow_html=True,
                )
                col3.markdown(
                    f'<div class="custom-row-space">{row["Time"]}</div>',
                    unsafe_allow_html=True,
                )
                col4.markdown(
                    f'<div class="custom-row-space">{row["Description"]}</div>',
                    unsafe_allow_html=True,
                )

                with col5:
                    change_but = st.button("Thay đổi", key=i)
                    if change_but:
                        if "app_id" not in st.session_state:
                            st.session_state.app_id = row["ID"]
                        if "app_doctor_id" not in st.session_state:
                            st.session_state.app_doctor_id = row["DoctorID"]
                        st.switch_page("./pages/update_appointment.py")

                with col6:
                    del_but = st.button("Hủy", key=row["ID"])
                    if del_but:
                        cancel_appointment(row["ID"])
                        st.experimental_rerun()

        else:
            st.write("Hiện không có lịch hẹn nào")
    else:
        st.session_state.clear()
        st.switch_page("main.py")
