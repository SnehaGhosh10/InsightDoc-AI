from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key or not gemini_api_key.strip():
    raise EnvironmentError("🚫 GEMINI_API_KEY not found or empty. Set it in your .env or Streamlit secrets.")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=gemini_api_key,
    temperature=0.0
)

# Embeddings and text splitter
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Utilities
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

def create_vectorstore_from_text(text):
    docs = text_splitter.create_documents([text])
    return FAISS.from_documents(docs, embeddings)

def answer_question(file, question):
    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        text = extract_text_from_docx(file)
    elif file.name.endswith(".txt"):
        text = extract_text_from_txt(file)
    else:
        return "⚠️ Unsupported file type. Please upload PDF, DOCX, or TXT."

    vectorstore = create_vectorstore_from_text(text)

    try:
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
        )
        result = qa.invoke({"query": question})
        return result.get("result", "⚠️ No result returned. Try a different question.")
    except Exception as e:
        return f"🚫 Retrieval error: {e}. Check GEMINI_API_KEY, network connection, or try a simpler question."
