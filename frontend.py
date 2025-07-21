import streamlit as st
from backend import answer_question

st.set_page_config(page_title="InsightDoc AI", layout="centered")
st.title("📄 InsightDoc AI - Document Q&A Chatbot")

# CSS for dark mode and chat-like display
st.markdown("""
    <style>
    body, .stApp { background-color: #000; color: #f5f5f5; }
    .stTextInput>div>div>input { background-color: #1e1e2f; color: #f5f5f5; }
    .stFileUploader>div>div>div>button,
    .stButton>button { background-color: #4c4c6c; color: #f5f5f5; }
    .chat-container { background-color: #121212; padding: 20px; border-radius: 12px; }
    .bot-message { background-color: #e0e0e0; color: #000; padding: 10px 15px; border-radius: 10px; margin-bottom: 10px; }
    .user-message { background-color: #1e1e2f; color: #f5f5f5; padding: 10px 15px; border-radius: 10px; margin-bottom: 10px; text-align: right; }
    </style>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📄 Upload your document (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])
question = st.text_input("💬 Ask a question about your document:")

if st.button("✨ Get Answer"):
    if uploaded_file and question:
        with st.spinner("🔍 Analyzing your document..."):
            answer = answer_question(uploaded_file, question)
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="user-message">{question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-message">{answer}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please upload a document and enter your question.")

