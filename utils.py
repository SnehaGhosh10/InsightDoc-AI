import pdfplumber
from docx import Document

def extract_text_from_pdf(file):
    """
    Extracts and returns plain text from a PDF file using pdfplumber.
    """
    try:
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if not text.strip():
            raise ValueError("No extractable text found in PDF (may be scanned/image-based).")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

def extract_text_from_docx(file):
    """
    Extracts and returns plain text from a DOCX file.
    """
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        if not text:
            raise ValueError("No extractable text found in DOCX.")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {e}")

def extract_text_from_txt(file):
    """
    Extracts and returns plain text from a TXT file with fallback decoding.
    """
    try:
        file_bytes = file.read()
        for encoding in ["utf-8", "latin-1", "cp1252"]:
            try:
                text = file_bytes.decode(encoding).strip()
                if text:
                    return text
            except UnicodeDecodeError:
                continue
        raise ValueError("Unsupported text encoding in TXT file.")
    except Exception as e:
        raise ValueError(f"Error extracting text from TXT: {e}")
