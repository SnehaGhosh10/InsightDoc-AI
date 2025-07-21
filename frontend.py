import streamlit as st
from backend import answer_question

# Page config
st.set_page_config(page_title="InsightDoc AI", page_icon="📄", layout="centered")

# Modern dark UI styling
st.markdown("""
    <style>
    body, .stApp { background-color: #0f0f0f; color: #e0e0e0; }
    h1, h2, h3, h4, h5, h6 { color: #ffffff; }
    .stTextInput > div > div > input {
        background-color: #1a1a2e; color: #ffffff;
        border-radius: 8px; padding: 10px; font-size: 16px;
    }
    .stFileUploader > div > div > div > button,
    .stButton > button {
        background: linear-gradient(90deg, #7209b7, #4361ee);
        color: #ffffff; font-weight: 600; border-radius: 8px;
        padding: 0.6em 1.2em; font-size: 16px; border: none;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #560bad, #4895ef);
    }
    .chat-container {
        background-color: #1a1a2e; padding: 20px; border-radius: 12px;
        max-height: 400px; overflow-y: auto; margin-top: 15px;
    }
    .user-message {
        background-color: #7209b7; color: #ffffff;
        padding: 10px 15px; border-radius: 10px;
        margin-bottom: 10px; max-width: 80%; margin-left: auto; text-align: right;
    }
    .bot-message {
        background-color: #4361ee; color: #ffffff;
        padding: 10px 15px; border-radius: 10px;
        margin-bottom: 10px; max-width: 80%;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>📄 InsightDoc AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #bbbbbb;'>Upload your document, ask questions, get instant AI answers</h4>", unsafe_allow_html=True)

# Upload and question input
uploaded_file = st.file_uploader("📄 Upload your document (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
question = st.text_input("💬 Ask a question about your document:", placeholder="Type your question here...")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Answer generation and display
if st.button("✨ Get Answer", disabled=not (uploaded_file and question)):
    with st.spinner("🔍 Analyzing your document, generating answer..."):
        answer = answer_question(uploaded_file, question)

    st.session_state["chat_history"].append(("user", question))
    st.session_state["chat_history"].append(("bot", answer))

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for sender, message in st.session_state["chat_history"]:
        css_class = "user-message" if sender == "user" else "bot-message"
        st.markdown(f'<div class="{css_class}">{message}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button("💾 Download Answer", answer, file_name="insightdoc_ai_answer.txt")
