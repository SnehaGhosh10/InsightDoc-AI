import cohere
import os
from groq import Groq

# Initialize clients only once (efficient)
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

cohere_client = cohere.Client(COHERE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def embed_document(text):
    """
    Generates an embedding for the provided text using Cohere.
    """
    response = cohere_client.embed(
        texts=[text],
        model="embed-english-light-v3.0"
    )
    return response.embeddings[0]

def generate_answer(messages):
    """
    Generates an assistant answer using Groq LLM based on the conversation history.
    """
    completion = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )
    return completion.choices[0].message.content

