import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import requests

from utils import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if groq_api_key is None:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

model = SentenceTransformer('all-MiniLM-L6-v2')


def split_text(text, max_chunk_size=500, overlap=50):
    def recursive_split(text):
        words = text.split()
        if len(words) <= max_chunk_size:
            return [text]
        midpoint = len(words) // 2 + overlap
        first_half = " ".join(words[:midpoint])
        second_half = " ".join(words[midpoint - overlap:])
        return recursive_split(first_half) + recursive_split(second_half)

    return recursive_split(text)


def create_faiss_index(chunks):
    embeddings = model.encode(chunks).astype('float32')
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, embeddings, chunks


def get_top_k_chunks(question, index, embeddings, chunks, k=3):
    question_embedding = model.encode([question]).astype('float32')
    distances, indices = index.search(question_embedding, k)
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

