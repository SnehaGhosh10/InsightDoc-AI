import cohere
import os
from groq import Groq

# Load API keys safely
CO_API_KEY = os.getenv("CO_API_KEY") or os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check and raise clear errors if missing
if CO_API_KEY is None:
    raise ValueError("🚨 CO_API_KEY not found in environment. Please set it in your .env or Streamlit Secrets.")
if GROQ_API_KEY is None:
    raise ValueError("🚨 GROQ_API_KEY not found in environment. Please set it in your .env or Streamlit Secrets.")

# Initialize clients
cohere_client = cohere.Client(CO_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def embed_document(text):
    response = cohere_client.embed(
        texts=[text],
        model="embed-english-light-v3.0"
    )
    return response.embeddings[0]

def generate_answer(messages):
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )
    return completion.choices[0].message.content



