import streamlit as st
from backend import answer_question

st.set_page_config(page_title="InsightDoc AI - Groq RAG", layout="centered")
st.title("📄 InsightDoc AI - Groq RAG Chatbot")

uploaded_file = st.file_uploader("📄 Upload your document (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
question = st.text_input("💬 Ask a question about your document:")

if st.button("✨ Get Answer"):
    if uploaded_file and question:
        with st.spinner("🔍 Analyzing and retrieving answer..."):
            answer = answer_question(uploaded_file, question)
        st.success("✅ Answer ready:")
        st.write(answer)
    else:
        st.warning("⚠️ Please upload a document and enter your question.")

