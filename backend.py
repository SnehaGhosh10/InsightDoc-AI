# backend.py

import pandas as pd
import PyPDF2
import docx
from utils import embed_document, generate_answer

# Store document text globally within module
stored_document_text = ""

def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif file.name.endswith(".docx"):
        doc_file = docx.Document(file)
        return " ".join(paragraph.text for paragraph in doc_file.paragraphs)
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
        return df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep=' ')
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        return ""

def upload_document(file):
    """
    Handles file upload and embedding.
    """
    global stored_document_text
    stored_document_text = extract_text(file)
    if stored_document_text:
        embed_document(stored_document_text)
        return "✅ Document uploaded and embedded."
    else:
        return "⚠️ Invalid or empty document."

def chat_with_document(user_message, chat_history):
    """
    Handles user queries using stored document context.
    """
    if stored_document_text == "":
        return "⚠️ Please upload a document first."
    prompt = f"Document: {stored_document_text}\n\nUser: {user_message}\n\nAnswer:"
    messages = chat_history + [{"role": "user", "content": prompt}]
    answer = generate_answer(messages)
    return answer
