import cohere
from dotenv import load_dotenv
import os

load_dotenv()  # Load the variables from the .env file
api_key = os.getenv("API_SECRET_KEY")
# Initialize the Cohere client
co = cohere.Client(api_key)  # Replace with your actual API key

def answer_question_with_cohere(context, question, max_tokens=100):
    """
    Answer a question based on the provided context using Cohere's text generation model.
    """
    # Create the QnA prompt
    prompt = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
    
    # Call the Cohere API
    response = co.generate(
        model="command-xlarge-nightly",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7
    )
    return response.generations[0].text.strip()
