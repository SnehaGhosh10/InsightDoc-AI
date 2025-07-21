# InsightDoc AI - frontend.py

import streamlit as st
from backend import answer_question

# Page configuration
st.set_page_config(page_title="InsightDoc AI", page_icon="📄", layout="centered")

# Custom CSS for sleek dark theme
st.markdown("""
    <style>
    body, .stApp {
        background-color: #0f0f0f;
        color: #e0e0e0;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a2e;
        color: #ffffff;
        border-radius: 8px;
    }
    .stFileUploader>div>div>div>button, .stButton>button {
        background: linear-gradient(90deg, #7209b7, #4361ee);
        color: #ffffff;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #560bad, #4895ef);
    }
    .chat-container {
        background-color: #1a1a2e;
        padding: 15px;
        border-radius: 12px;
        max-height: 400px;
        overflow-y: auto;
    }
    .bot-message {
        background-color: #4361ee;
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
    }
    .user-message {
        background-color: #7209b7;
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        max-width: 80%;
        margin-left: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 style='text-align: center;'>📄 InsightDoc AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #aaaaaa;'>Upload documents and ask questions powered by Groq + FAISS</h4>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📄 Upload your document (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"], key="uploaded_file")

# Question input
question = st.text_input("💬 Ask a question about your document:", placeholder="Type your question here...", key="question")

# Answer display
if st.button("✨ Get Your Answer"):
    if uploaded_file and question:
        with st.spinner("🔍 Generating your answer..."):
            answer = answer_question(uploaded_file, question)
        # Chat-like display
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="user-message">{question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-message">{answer}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Download answer
        st.download_button("💾 Download Answer", answer, file_name="InsightDoc_Answer.txt")
    else:
        st.warning("⚠️ Please upload a document and enter your question.")

# Clear button using session state
if st.button("🔄 Clear"):
    for key in st.session_state.keys():
        st.session_state[key] = None
    st.experimental_rerun()
