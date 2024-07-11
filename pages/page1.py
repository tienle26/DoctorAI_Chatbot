import streamlit as st
from streamlit_navigation_bar import st_navbar
import pandas as pd
from connect import get_data, create_credentials
from page_functions import home, search_drugs, appointment, profile
from crud import filter_appointment, cancel_appointment
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.question_answering import load_qa_chain


create_credentials()
st.set_page_config(page_title="Use", page_icon="👨‍🔬", layout="wide")
navbar = st_navbar(
    ["Home", "Chat", "Search", "Appointment", "Profile", "Logout"],
    selected=st.session_state.default_page,
)


@st.cache_resource
def load_data():
    # df = get_data("Doctor")
    # df.to_csv("Doctor.csv", index=False)
    loader = CSVLoader(file_path="Doctor.csv", encoding="utf8")
    data = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)

    chunks = splitter.split_documents(data)

    embeddings = HuggingFaceEmbeddings()

    vector_index = Chroma.from_documents(chunks, embeddings)
    print("Loading data success..")

    return vector_index, chunks


def display(vector_index, chunks):
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)

    df = get_data("Account")
    use = df[df["ID"] == st.session_state.ID].iloc[0]["Use"]

    if use == 1:
        if (
            "messages" not in st.session_state.keys()
        ):  # Initialize the chat message history
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Xin chào ! Tôi có thể giúp gì cho bạn 🧑‍⚕️ ?.",
                }
            ]

        if "question_count" not in st.session_state:  # Initialize the question count
            st.session_state.question_count = 0

        if question := st.chat_input(
            "Your question"
        ):  # Prompt for user input and save to chat history
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.question_count += 1

        for message in st.session_state.messages:  # Display the prior chat messages
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):

                    if st.session_state.question_count <= 5:
                        prompt_template = """
                    Bạn là một chatbot y tế chuyên nghiệp.
                    Trả lời tự nhiên như 1 người bạn.
                    Trả lời đầy đủ thông tin dựa vào ngữ cảnh.
                    Tư vấn sức khỏe và đưa ra lời khuyên cho bệnh nhân.
                    Recommend thuốc cho bệnh nhân.
                    Gợi ý một số bác sĩ liên quan đến tình trạng bệnh nhân nếu cần.
                    
                    Context:\n {context}?\n
                    Question: \n {question}\n
                    Answer:
                    """
                        context = vector_index.similarity_search(question, k=3)
                        prompt = PromptTemplate(
                            template=prompt_template,
                            input_variables=["context", "question"],
                        )
                        model = ChatGoogleGenerativeAI(
                            model="gemini-1.5-flash-latest",
                            google_api_key=GOOGLE_API_KEY,
                            temperature=0.3,
                        )
                        chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
                        response = chain(
                            {"input_documents": chunks, "question": question},
                            return_only_outputs=True,
                        )
                        st.write(response["output_text"])
                        message = {
                            "role": "assistant",
                            "content": response["output_text"],
                        }
                        st.session_state.messages.append(
                            message
                        )  # Add response to message history

                    else:
                        st.write("Bạn vui lòng thanh toán để được tư vấn tiếp.")
                        st.write(
                            "Link thanh toán: https://buy.stripe.com/test_fZecPd1H73zz7jqfYZ"
                        )
                        st.write(
                            "Hoặc thanh toán qua tài khoản: Nguyễn Văn Mai- tài khoản: 138608649. Ngân hàng ACB chi nhánh sài gòn "
                        )
                        st.write(
                            "Lưu ý: từ câu hỏi thứ 5, phí 50k/câu. Từ câu thứ 10, phí 100k/ câu"
                        )
                        st.write("Bạn có muốn tiếp tục nữa không ?")
                        update_user2(PatientID, use=0)

                        col_1, col_2 = st.columns(2)
                        k = 0
                        with col_1:
                            y = st.button("Yes")
                            if y == True:
                                k = 1

                        with col_2:
                            n = st.button("No")
                            if n == True:
                                k = 2
                        if k == 1:
                            st.write("Thật tuyệt !!....")
                            st.session_state.question_count = 0
                            st.empty()
                        if k == 2:
                            st.write("Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi !!")
    if use == 0:
        st.write("Bạn vui lòng thanh toán để được tư vấn tiếp.")
        st.write("Link thanh toán: https://buy.stripe.com/test_fZecPd1H73zz7jqfYZ")
        st.write(
            "Hoặc thanh toán qua tài khoản: Nguyễn Văn Mai- tài khoản: 138608649. Ngân hàng ACB chi nhánh sài gòn "
        )
        st.write("Lưu ý: từ câu hỏi thứ 5, phí 50k/câu. Từ câu thứ 10, phí 100k/ câu")
        st.write("Bạn có muốn tiếp tục nữa không ?")
        col_1, col_2 = st.columns(2)
        k = 0
        with col_1:
            y = st.button("Yes")
            if y == True:
                k = 1

        with col_2:
            n = st.button("No")
            if n == True:
                k = 2
        if k == 1:
            st.write("Thật tuyệt !!....")
            st.session_state.question_count = 0
            st.empty()
            use = 1

        if k == 2:
            st.write("Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi !!")


if navbar == "Home":
    home()

elif navbar == "Chat":
    vector_index, chunks = load_data()
    display(vector_index, chunks)


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
