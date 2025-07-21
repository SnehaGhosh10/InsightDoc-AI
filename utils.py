from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_pdf(file):
    """
    Extracts and returns plain text from a PDF file with safe error handling.
    """
    try:
        text = ""
        reader = PdfReader(file)
        if reader.is_encrypted:
            try:
                reader.decrypt('')
            except:
                raise ValueError("The PDF file is encrypted and cannot be read.")
        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text
        if not text.strip():
            raise ValueError("No extractable text found in the PDF.")
        print(f"[DEBUG] Extracted {len(text)} characters from PDF: {file.name}")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")

def extract_text_from_docx(file):
    """
    Extracts and returns plain text from a DOCX file with safe error handling.
    """
    try:
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        if not text.strip():
            raise ValueError("No extractable text found in the DOCX file.")
        print(f"[DEBUG] Extracted {len(text)} characters from DOCX: {file.name}")
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {e}")

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
                    print(f"[DEBUG] Extracted {len(text)} characters from TXT: {file.name} using {encoding}")
                    return text
            except UnicodeDecodeError:
                continue
        raise ValueError("Unsupported text encoding in TXT file.")
    except Exception as e:
        raise ValueError(f"Failed to extract text from TXT: {e}")


