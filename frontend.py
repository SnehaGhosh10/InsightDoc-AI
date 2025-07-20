import streamlit as st
from backend import answer_question

# Page config with your brand
st.set_page_config(page_title="InsightDoc AI", layout="centered")
st.title("📄 InsightDoc AI - Document Q&A Chatbot")

# Inject dark theme + colorful chat bubble styles
st.markdown("""
    <style>
    .chat-container {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 12px;
        color: #f5f5f5;
    }
    .bot-message {
        background-color: #3c3c5c;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: #f5f5f5;
    }
    .user-message {
        background-color: #4c4c6c;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        color: #f5f5f5;
    }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📄 Upload your document (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
question = st.text_input("💬 Ask a question about your document:")

if st.button("✨ Get Answer"):
    if uploaded_file and question:
        with st.spinner("🔍 Analyzing your document..."):
            answer = answer_question(uploaded_file, question)

        # Display chatbot-like conversation
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="user-message">{question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-message">{answer}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a document and enter your question.")

