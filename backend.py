import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import requests

from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

model = SentenceTransformer('all-MiniLM-L6-v2')

# Chunk splitting
def split_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def create_faiss_index(chunks):
    embeddings = model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index, embeddings, chunks

def get_top_k_chunks(question, index, embeddings, chunks, k=3):
    question_embedding = model.encode([question])
    distances, indices = index.search(np.array(question_embedding), k)
    retrieved_chunks = [chunks[idx] for idx in indices[0]]
    return retrieved_chunks

def call_groq_llm(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groq_api_key}"
    }
    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful document Q&A assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"⚠️ Error: {response.status_code} - {response.text}"

def answer_question(file, question):
    try:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        elif file.name.endswith(".txt"):
            text = extract_text_from_txt(file)
        else:
            return "❌ Unsupported file type."

        if not text:
            return "❌ No text could be extracted from the document."

        chunks = split_text(text)
        index, embeddings, chunks_list = create_faiss_index(chunks)
        top_chunks = get_top_k_chunks(question, index, embeddings, chunks_list, k=3)

        context = "\n".join(top_chunks)
        prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer concisely based on the context above."

        answer = call_groq_llm(prompt)
        return answer
    except Exception as e:
        return f"⚠️ An error occurred: {e}"


