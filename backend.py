from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise EnvironmentError("🚫 GROQ_API_KEY not found in environment variables.")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model_name="llama3-8b-8192",
    temperature=0
)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Extract text utility
from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

def create_vectorstore_from_text(text):
    docs = text_splitter.create_documents([text])
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def answer_question(file, question):
    if file.name.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    elif file.name.endswith(".docx"):
        text = extract_text_from_docx(file)
    elif file.name.endswith(".txt"):
        text = extract_text_from_txt(file)
    else:
        return "Unsupported file type."

    vectorstore = create_vectorstore_from_text(text)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    result = qa.invoke({"query": question})
    return result["result"]

