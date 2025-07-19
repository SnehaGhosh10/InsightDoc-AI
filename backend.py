from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Groq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from utils import extract_text

# Load environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = Groq(
    model_name="llama3-8b-8192",
    api_key=groq_api_key
)

# Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def answer_question(uploaded_file, question):
    # Extract and split text
    text = extract_text(uploaded_file)
    docs = text_splitter.create_documents([text])

    # Vector DB
    vectorstore = Chroma.from_documents(docs, embeddings)

    retriever = vectorstore.as_retriever()

    # RAG QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )

    result = qa_chain({"query": question})
    return result["result"]
