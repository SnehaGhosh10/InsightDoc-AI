import streamlit as st
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt
from backend import answer_question

st.set_page_config(page_title="🗂️ Document Q&A Chatbot", layout="centered")
st.title("🗂️ Document Q&A Chatbot with RAG")
st.markdown("Upload a document, ask questions, and get instant answers powered by Groq + Hugging Face embeddings.")

uploaded_file = st.file_uploader("📂 Upload your document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
question = st.text_input("❓ Enter your question")

if st.button("🚀 Get Answer"):
    if uploaded_file and question.strip():
        with st.spinner("🤖 Reading your document, building retrieval index, and thinking..."):
            file_type = uploaded_file.name.split(".")[-1].lower()
            if file_type == "pdf":
                document_text = extract_text_from_pdf(uploaded_file)
            elif file_type == "docx":
                document_text = extract_text_from_docx(uploaded_file)
            elif file_type == "txt":
                document_text = extract_text_from_txt(uploaded_file)
            else:
                st.error("Unsupported file type.")
                st.stop()

            if not document_text.strip():
                st.error("The document appears empty or could not be read.")
                st.stop()

            answer = answer_question(document_text, question)
            st.success("✅ Answer Generated!")
            st.write(answer)
    else:
        st.warning("Please upload a document and enter your question.")

st.markdown("---")
st.caption("🚀 Built with ❤️ using Streamlit + Groq + Hugging Face for fast, insightful document Q&A.")
