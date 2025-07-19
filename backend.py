from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils import embed_document, generate_answer
import pandas as pd
import PyPDF2
import docx

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    user_message: str
    chat_history: list

stored_document_text = ""

def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        return " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return " ".join(para.text for para in doc.paragraphs)
    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file.file)
        return df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.cat(sep=' ')
    elif file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        return ""

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    global stored_document_text
    stored_document_text = extract_text(file)
    if stored_document_text:
        embed_document(stored_document_text)
        return {"message": "Document uploaded and embedded."}
    return {"message": "Invalid or empty document."}

@app.post("/chat/")
async def chat(req: QueryRequest):
    if stored_document_text == "":
        return {"answer": "Please upload a document first."}
    messages = req.chat_history + [{"role": "user", "content": f"Document: {stored_document_text}\n\nUser: {req.user_message}\n\nAnswer:"}]
    answer = generate_answer(messages)
    return {"answer": answer}