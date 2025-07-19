import streamlit as st
from backend import answer_question

st.set_page_config(page_title="🗂️ Document Q&A Chatbot", layout="centered")
st.title("🗂️ Document Q&A Chatbot with RAG")

st.markdown(
    "Upload a **PDF, DOCX, or TXT document** and ask any question related to its contents."
)

uploaded_file = st.file_uploader("📄 Upload your document", type=["pdf", "docx", "txt"])
question = st.text_input("❓ Enter your question here")

if st.button("🚀 Get Answer"):
    if uploaded_file and question.strip():
        with st.spinner("🤖 Reading your document and finding the answer..."):
            try:
                answer = answer_question(uploaded_file, question)
                st.success("✅ Answer Generated:")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    else:
        st.warning("⚠️ Please upload a document and enter a question.")

st.markdown("---")
st.caption("🚀 Powered by Groq LLM + Hugging Face Embeddings + LangChain + Streamlit.")
