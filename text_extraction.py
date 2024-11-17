import fitz  # PyMuPDF
import os
from docx import Document

def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_txt(file):
    """Extract text from a TXT file."""
    return file.read().decode('utf-8')  # Decode the uploaded binary file to a string

def extract_text_from_docx(file):
    """Extract text from a DOCX file."""
    doc = Document(file)
    # Collect paragraphs, stripping excess whitespace
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)

def extract_text(file, file_type):
    """Extract text based on file type."""
    if file_type == "pdf":
        text = extract_text_from_pdf(file)
    elif file_type == "txt":
        text = extract_text_from_txt(file)
    elif file_type == "docx":
        text = extract_text_from_docx(file)
    else:
        raise ValueError("Unsupported file type")
    
    # Ensure extracted text is valid
    if not text or not isinstance(text, str):
        raise ValueError("Failed to extract text from the uploaded document.")
    
    return text

