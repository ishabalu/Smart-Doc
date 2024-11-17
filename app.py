import re
from text_extraction import extract_text_from_pdf
from text_summarization import summarize_long_text_cohere  # Use the Cohere summarizer
from qa_system import answer_question_with_cohere  # Updated import


def preprocess_text(raw_text):
    """
    Clean and preprocess extracted text from any document type.
    """
    # Remove multiple spaces, newlines, and tabs
    cleaned_text = re.sub(r'\s+', ' ', raw_text)  
    
    # Remove common document artifacts (e.g., "Page X of Y")
    cleaned_text = re.sub(r'Page \d+ of \d+', '', cleaned_text)  
    
    # Strip leading and trailing whitespace
    cleaned_text = cleaned_text.strip()
    
    # Remove extra artifacts specific to DOCX (if observed, customize as needed)
    cleaned_text = re.sub(r'\x0c', '', cleaned_text)  # Form feed characters
    return cleaned_text



def main():
    # Path to your test document
    pdf_path = "data/sample.pdf"
    
    # Extract text from the PDF
    raw_text = extract_text_from_pdf(pdf_path)
    print("Raw Extracted Text:")
    print(raw_text)
    
    # Preprocess the extracted text
    preprocessed_text = preprocess_text(raw_text)
    print("\nPreprocessed Text:")
    print(preprocessed_text)

    # Summarize the text using Cohere API
    print("\nGenerating Summary...")
    final_summary = summarize_long_text_cohere(preprocessed_text)  # Use Cohere summarization function
    print("\nSummary:")
    print(final_summary)

    # Answer a question using the extracted text
    question = "Which companies dominate the premium smartphone market?"
    print(f"\nQuestion: {question}")
    answer = answer_question_with_cohere(preprocessed_text, question)  # Use Cohere QnA
    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()
