import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    """Extract text from a PDF file-like object."""
    text = ""
    # Open the file using fitz with its file-like object (stream)
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            text += page.get_text()
    return text
