import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"
st.title("📄InsightDoc AI: Multi-Doc QA Chatbot")

uploaded_file = st.file_uploader("Upload a PDF, DOCX, XLSX, or TXT", type=["pdf", "docx", "xlsx", "txt"])
if uploaded_file:
    with st.spinner("Uploading and processing..."):
        res = requests.post(f"{FASTAPI_URL}/upload/", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
        st.success(res.json()["message"])

st.write("### Chat with your document:")
if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask something about the document")
if user_input:
    with st.spinner("Thinking..."):
        payload = {"user_message": user_input, "chat_history": st.session_state.history}
        res = requests.post(f"{FASTAPI_URL}/chat/", json=payload)
        answer = res.json()["answer"]
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": answer})
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(answer)
