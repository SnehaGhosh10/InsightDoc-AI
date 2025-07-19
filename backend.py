from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import Groq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = Groq(api_key=groq_api_key, model_name="llama3-8b-8192", temperature=0)

# Initialize Hugging Face embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print(embeddings.embed_query("Test"))
# Prompt template (clean)
template = """
You are a helpful assistant. Answer the user's question using ONLY the context provided.

Context:
{context}

Question:
{question}

Answer in simple, clear, direct language.
"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template
)

def process_and_create_retriever(document_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.create_documents([document_text])

    vectordb = Chroma.from_documents(texts, embedding=embeddings, persist_directory="./chroma_db")
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})
    return retriever

def answer_question(document_text, question):
    retriever = process_and_create_retriever(document_text)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    result = qa_chain({"query": question})
    return result["result"]
