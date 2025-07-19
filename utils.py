from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(uploaded_file):
    try:
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(uploaded_file):
    try:
        doc = docx.Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def extract_text_from_txt(uploaded_file):
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Error reading TXT: {str(e)}"

def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    else:
        return "❌ Unsupported file type. Please upload PDF, DOCX, or TXT."




