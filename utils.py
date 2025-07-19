import cohere
import os
from groq import Groq

def embed_document(text):
    co = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = co.embed(texts=[text], model="embed-english-light-v3.0")
    return response.embeddings[0]

def generate_answer(messages):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )
    return completion.choices[0].message.content
