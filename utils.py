from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file):
    try:
        text = ""
        reader = PdfReader(file)
        if reader.is_encrypted:
            try:
                reader.decrypt('')
            except:
                raise ValueError("PDF is encrypted and cannot be read.")
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        if not text.strip():
            raise ValueError("No extractable text found in PDF.")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

def extract_text_from_docx(file):
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        if not text:
            raise ValueError("No extractable text found in DOCX.")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {e}")

def extract_text_from_txt(file):
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
