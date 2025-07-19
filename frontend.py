import streamlit as st
from backend import answer_question

st.set_page_config(page_title="🗂️ Document Q&A Chatbot", layout="centered")
st.title("🗂️ Document Q&A Chatbot with RAG (FAISS)")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
question = st.text_input("Ask a question about your document:")

if st.button("Get Answer"):
    if uploaded_file and question:
        with st.spinner("Analyzing..."):
            answer = answer_question(uploaded_file, question)
        st.success("Answer:")
        st.write(answer)
    else:
        st.warning("Please upload a document and enter your question.")
