import cohere
from dotenv import load_dotenv
import os

load_dotenv()  # Load the variables from the .env file
api_key = os.getenv("API_SECRET_KEY")


# Initialize the Cohere client with your API key
co = cohere.Client(api_key) 

def summarize_text_cohere(text, max_tokens=300):
    """
    Summarize the input text using Cohere's text generation model.
    """
    # Create the summarization prompt
    prompt = f"Summarize the following document concisely:\n\n{text}"
    
    # Call the Cohere API to generate a summary
    response = co.generate(
        model="command-xlarge-nightly",  # Model optimized for summarization
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.7,  # Lower temperature for deterministic output
        stop_sequences=["--"]  # Optional: Stop generation at specific sequences
    )
    return response.generations[0].text.strip()

def summarize_long_text_cohere(text, max_chunk_tokens=3000, max_tokens=300):
    """
    Summarize long text by splitting it into chunks if necessary and combining results.
    """
    # Split text into manageable chunks
    words = text.split()
    chunks = [" ".join(words[i:i + max_chunk_tokens]) for i in range(0, len(words), max_chunk_tokens)]
    
    # Summarize each chunk
    chunk_summaries = [summarize_text_cohere(chunk, max_tokens=max_tokens) for chunk in chunks]
    
    # Combine summaries
    combined_summary = " ".join(chunk_summaries)
    
    # Optionally, summarize the combined summary for a final cohesive result
    if len(chunk_summaries) > 1:
        final_summary = summarize_text_cohere(combined_summary, max_tokens=max_tokens)
        return final_summary
    
    return combined_summary
