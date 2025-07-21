import streamlit as st
from backend import answer_question

# Page config with your brand
st.set_page_config(page_title="InsightDoc AI", page_icon="📄", layout="centered")

# Custom CSS for cool dark UI with accent colors and visible labels
st.markdown("""
    <style>
    body, .stApp {
        background-color: #0f0f0f;
        color: #e0e0e0;
    }
    label, .stTextInput label, .stFileUploader label {
        color: #e0e0e0 !important;
        font-weight: 500;
    }
    .stTextInput>div>div>input {
        background-color: #1a1a2e;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px;
    }
    .stFileUploader>div>div>div>button {
        background-color: #3a0ca3;
        color: #ffffff;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(90deg, #7209b7, #4361ee);
        color: #ffffff;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6em 1.2em;
        font-size: 16px;
        cursor: pointer;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #560bad, #4895ef);
        transform: scale(1.02);
    }
    .chat-container {
        background-color: #1a1a2e;
        padding: 20px;
        border-radius: 12px;
        color: #ffffff;
        max-height: 400px;
        overflow-y: auto;
        margin-top: 15px;
    }
    .bot-message {
        background-color: #4361ee;
        color: #ffffff;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #7209b7;
        color: #ffffff;
        padding: 10px 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
        align-self: flex-end;
        max-width: 80%;
        word-wrap: break-word;
        margin-left: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Title with emoji for branding
st.markdown("""
    <h1 style='text-align: center;'>📄 InsightDoc AI</h1>
    <h3 style='text-align: center; color: #a0a0a0;'>Ask your documents, get instant AI answers</h3>
""", unsafe_allow_html=True)

# File uploader with clear label
uploaded_file = st.file_uploader("📄 Upload your document (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])

# Text input with placeholder for guidance
question = st.text_input("💬 Ask a question about your document:", placeholder="Type your question here...")

# Main action button with clear call to action
if st.button("✨ Get Your Answer"):
    if uploaded_file and question:
        with st.spinner("🔍 Analyzing your document and generating your answer..."):
            answer = answer_question(uploaded_file, question)

        # Chat container for displaying Q&A
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="user-message">{question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-message">{answer}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Download option for answer
        st.download_button("💾 Download Answer", answer, file_name="InsightDoc_AI_Answer.txt")

    else:
        st.warning("⚠️ Please upload a document and enter your question to proceed.")

# Optional clear/reset button
if st.button("🔄 Clear All"):
    st.experimental_rerun()
