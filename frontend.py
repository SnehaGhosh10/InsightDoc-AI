import streamlit as st
from backend import upload_document, chat_with_document

st.title("📄 InsightDoc AI: Multi-Doc QA Chatbot ")

# Upload document
uploaded_file = st.file_uploader("Upload a PDF, DOCX, XLSX, or TXT", type=["pdf", "docx", "xlsx", "txt"])

if uploaded_file:
    with st.spinner("Uploading and processing..."):
        message = upload_document(uploaded_file)
        st.success(message)

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

st.write("### Chat with your document:")

# Chat input
user_input = st.chat_input("Ask something about the document")
if user_input:
    with st.spinner("Generating response..."):
        answer = chat_with_document(user_input, st.session_state.history)
        # Update chat history
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": answer})
        # Display chat messages
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(answer)
