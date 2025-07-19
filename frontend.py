import streamlit as st
from backend import upload_document, chat_with_document

st.set_page_config(page_title="InsightDoc AI", page_icon="📄")
st.title("📄 InsightDoc AI: Multi-Doc QA Chatbot")

st.markdown(
    """
    Upload **PDF, DOCX, XLSX, or TXT** files and chat with your documents instantly using Groq + Cohere powered retrieval-augmented generation.
    """
)

# Document Upload Section
uploaded_file = st.file_uploader(
    "Upload a PDF, DOCX, XLSX, or TXT file to begin:",
    type=["pdf", "docx", "xlsx", "txt"]
)

if uploaded_file:
    with st.spinner("📄 Uploading and processing your document..."):
        message = upload_document(uploaded_file)
        st.success(message)

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

st.divider()
st.subheader("💬 Chat with your document")

# Chat input
user_input = st.chat_input("Ask something about the uploaded document")

if user_input:
    with st.spinner("💡 Generating response..."):
        answer = chat_with_document(user_input, st.session_state.history)
        
        # Update session chat history
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.history.append({"role": "assistant", "content": answer})

        # Display chat messages cleanly
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(answer)

