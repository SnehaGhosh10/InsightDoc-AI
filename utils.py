
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += (page.extract_text() or "") + "\n"
        return text.strip()
    except Exception as e:
        return f"⚠️ PDF extraction error: {e}"

def extract_text_from_docx(file):
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"⚠️ DOCX extraction error: {e}"

def extract_text_from_txt(file):
    try:
        text = file.read()
        if isinstance(text, bytes):
            text = text.decode("utf-8", errors="ignore")
        return text.strip()
    except Exception as e:
        return f"⚠️ TXT extraction error: {e}"


