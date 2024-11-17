import re
from text_extraction import extract_text_from_pdf
from text_summarization import summarize_long_text_cohere  # Use the Cohere summarizer
from qa_system import answer_question_with_cohere  # Updated import


def preprocess_text(raw_text):
    """
    Clean and preprocess extracted text.
    """
    cleaned_text = re.sub(r'\s+', ' ', raw_text)  # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'Page \d+ of \d+', '', cleaned_text)  # Remove page numbers
    return cleaned_text.strip()


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
