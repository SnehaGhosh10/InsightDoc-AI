### InsightDoc AI - Stable, Clean Backend with GROQ Key Handling ###

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
import os


from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise EnvironmentError("🚫 GROQ_API_KEY not found. Please set it in your environment or .env file.")

# Initialize Groq LLM safely
try:
    llm = ChatGroq(api_key=groq_api_key, model_name="llama3-8b-8192", temperature=0)
except Exception as e:
    raise EnvironmentError(f"🚫 Failed to initialize Groq LLM: {e}. Check your API key and billing.")

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Import your utils (ensure utils.py has these implemented correctly)
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

def create_vectorstore_from_text(text):
    """Split and embed document text into a FAISS vector store."""
    docs = text_splitter.create_documents([text])
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def answer_question(file, question):
    """Main function to extract text, embed, retrieve, and answer."""
    try:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        elif file.name.endswith(".txt"):
            text = extract_text_from_txt(file)
        else:
            return "⚠️ Unsupported file type. Please upload PDF, DOCX, or TXT."

        vectorstore = create_vectorstore_from_text(text)

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )

        result = qa.invoke({"query": question})
        return result.get("result", "⚠️ No result returned. Try a different question.")

    except Exception as e:
        return f"🚫 Retrieval error: {e}. Check GROQ_API_KEY, network connection, or try a simpler question."

### End of stable backend code for InsightDoc AI ###

