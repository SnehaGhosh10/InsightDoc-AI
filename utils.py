from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    """
    Extracts and returns plain text from a PDF file.
    """
    text = ""
    reader = PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() or ""
    return text.strip()


def extract_text_from_docx(file):
    """
    Extracts and returns plain text from a DOCX file.
    """
    doc = Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()


def extract_text_from_txt(file):
    """
    Extracts and returns plain text from a TXT file.
    """
    return file.read().decode("utf-8").strip()

