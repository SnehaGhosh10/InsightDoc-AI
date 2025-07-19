import pandas as pd
import PyPDF2
import docx
from utils import embed_document, generate_answer

# Store document text globally within the module
stored_document_text = ""

def extract_text(file):
    """
    Extracts text from PDF, DOCX, XLSX, or TXT files.
    """
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
    Handles file upload, extraction, and embedding generation using Cohere.
    """
    global stored_document_text
    stored_document_text = extract_text(file)
    if stored_document_text.strip():
        embed_document(stored_document_text)
        return "✅ Document uploaded and embedded."
    else:
        return "⚠️ Invalid or empty document. Please upload a valid PDF, DOCX, XLSX, or TXT file."

def chat_with_document(user_message, chat_history):
    """
    Handles user queries over the stored document using Groq for response generation.
    """
    if not stored_document_text.strip():
        return "⚠️ Please upload a document first."

    # Compose structured prompt for Groq:
    prompt = (
        f"You are a document QA assistant. "
        f"Use the following document content to answer concisely:\n\n"
        f"Document Content:\n{stored_document_text[:3000]}...\n\n"  # limit context size for Groq
        f"User Question: {user_message}\n\n"
        f"Answer:"
    )

    # Add to chat history
    messages = chat_history + [{"role": "user", "content": prompt}]
    answer = generate_answer(messages)
    return answer

