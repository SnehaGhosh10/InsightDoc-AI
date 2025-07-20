import streamlit as st
from backend import answer_question

# Page config with your brand
st.set_page_config(page_title="InsightDoc AI", layout="centered")
st.title("📄 InsightDoc AI - Document Q&A Chatbot")

# Inject black background + light chat message colors
st.markdown("""
    <style>
    body, .stApp {
        background-color: #000000;
        color: #f5f5f5;
    }
    .chat-container {
        background-color: #121212;
        padding: 20px;
        border-radius: 12px;
        color: #f5f5f5;
    }
    .bot-message {
        background-color: #e0e0e0;
        color: #000000;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #f5f5f5;
        color: #000000;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        align-self: flex-end;
        max-width: 80%;
        word-wrap: break-word;
    }
    .stTextInput>div>div>input {
        background-color: #1e1e2f;
        color: #f5f5f5;
    }
    .stFileUploader>div>div>div>button {
        background-color: #3c3c5c;
        color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4c4c6c;
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

        # Display chatbot-like conversation with light message bubbles
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="user-message">{question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-message">{answer}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a document and enter your question.")
