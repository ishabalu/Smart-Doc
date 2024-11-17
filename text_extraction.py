import fitz  # PyMuPDF
import os
from docx import Document
import pandas as pd 


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

def extract_text_from_excel(file):
    """Extract text from an Excel file."""
    try:
        # Load the Excel file into a DataFrame
        df = pd.read_excel(file)

        # Convert the DataFrame to a single string
        text = ""
        for col in df.columns:
            text += f"Column: {col}\n"  # Include column headers
            text += "\n".join(df[col].dropna().astype(str))  # Include all non-NaN values in the column
            text += "\n\n"  # Add spacing between columns

        return text.strip()  # Return the combined text
    except Exception as e:
        raise ValueError(f"Failed to extract text from the Excel file. Error: {e}")

def extract_text(file, file_type):
    """Extract text based on file type."""
    if file_type == "pdf":
        text = extract_text_from_pdf(file)
    elif file_type == "txt":
        text = extract_text_from_txt(file)
    elif file_type == "docx":
        text = extract_text_from_docx(file)
    elif file_type in ["xls", "xlsx"]: 
        text = extract_text_from_excel(file)
    else:
        raise ValueError("Unsupported file type")
    
    # Ensure extracted text is valid
    if not text or not isinstance(text, str):
        raise ValueError("Failed to extract text from the uploaded document.")
    
    return text

