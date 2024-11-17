import re
import streamlit as st
from text_extraction import extract_text_from_pdf
from text_summarization import summarize_long_text_cohere
from qa_system import answer_question_with_cohere
from textblob import TextBlob
import plotly.graph_objects as go

# Helper Functions
def preprocess_text(raw_text):
    """Clean and preprocess extracted text."""
    cleaned_text = re.sub(r'\s+', ' ', raw_text)
    cleaned_text = re.sub(r'Page \d+ of \d+', '', cleaned_text)
    return cleaned_text.strip()

def analyze_sentiment(text):
    """Analyze sentiment and return polarity and tone."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        tone = "Positive"
    elif polarity < -0.1:
        tone = "Negative"
    else:
        tone = "Neutral"
    return polarity, tone

def create_gauge(polarity, tone):
    """Create a smaller speedometer-like gauge."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=polarity,
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': "black"},
            'steps': [
                {'range': [-1, -0.1], 'color': "red"},
                {'range': [-0.1, 0.1], 'color': "yellow"},
                {'range': [0.1, 1], 'color': "green"}
            ],
        },
        title={'text': f"Tone: {tone}"}
    ))

    # Adjust layout for a smaller size
    fig.update_layout(
        width=280,  # Set the width of the figure
        height=280,  # Set the height of the figure
        margin=dict(t=10, b=10, l=10, r=10)  # Reduce margins for compactness
    )

    return fig

# Custom Styles
st.markdown(
    """
    <style>
    body {
        background-color: #1c1e21; /* Dark background for a clean look */
        color: #e8e8e8; /* Light text for contrast */
    }
    .title {
        text-align: center; 
        font-size: 42px; 
        font-family: 'Arial', sans-serif; 
        color: #4CAF50; 
        margin-bottom: 20px;
    }
    .steps {
        font-size: 20px; 
        line-height: 1.8; 
        color: #e8e8e8; 
        font-family: 'Arial', sans-serif;
        margin-top: 20px;
        text-align: left;
    }
    .upload-section {
        text-align: center; 
        font-size: 20px; 
        margin-top: 30px; 
        padding: 20px;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        background-color: #2a2d31; /* Slightly lighter background for contrast */
        color: #ffffff;
        font-family: 'Arial', sans-serif;
        cursor: pointer;
    }
    .upload-section:hover {
        background-color: #333333;
        border-color: #FFDC5A; /* Golden yellow on hover */
    }
    .footer {
        text-align: center; 
        font-size: 14px; 
        margin-top: 50px; 
        color: #a9a9a9;
    }
    .highlight {
        color: #FFDC5A; /* Golden yellow for highlighting important elements */
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title Section
st.markdown('<div class="title">Smart Document Summarizer and Q&A System</div>', unsafe_allow_html=True)

# Steps to Use Section
st.markdown(
    """
    <div class="steps">
    <strong>Steps to Use:</strong> <br><br>
    <span class="highlight">1.</span> Upload a PDF document using the uploader below.<br>
    <span class="highlight">2.</span> View the extracted text or summary in the respective sections.<br>
    <span class="highlight">3.</span> Type a question to interact with the Q&A system.
    </div>
    """,
    unsafe_allow_html=True,
)

# File Upload Section
uploaded_file = st.file_uploader(
    label="",
    type="pdf",
    label_visibility="visible"
)

# Initialize Session State
if "preprocessed_text" not in st.session_state:
    st.session_state["preprocessed_text"] = None

if "summary" not in st.session_state:
    st.session_state["summary"] = None

if "sentiment" not in st.session_state:
    st.session_state["sentiment"] = None

if "qa_history" not in st.session_state:
    st.session_state["qa_history"] = []

if "current_question" not in st.session_state:
    st.session_state["current_question"] = None

if "current_answer" not in st.session_state:
    st.session_state["current_answer"] = None

# Process Uploaded File
if uploaded_file is not None:
    st.info(f"**Uploaded File:** {uploaded_file.name} ({uploaded_file.size} bytes)")

    if st.session_state["preprocessed_text"] is None:
        # Extract and Preprocess Text
        with st.spinner("🔍 Extracting text... Please wait."):
            raw_text = extract_text_from_pdf(uploaded_file)
            st.session_state["preprocessed_text"] = preprocess_text(raw_text)

    # Toggleable Extracted Text Section
    with st.expander("📜 View Extracted Text"):
        st.write(st.session_state["preprocessed_text"])

    # Sentiment Analysis Section
    if st.session_state["sentiment"] is None:
        with st.spinner("🧠 Analyzing sentiment... Hang tight!"):
            polarity, tone = analyze_sentiment(st.session_state["preprocessed_text"])
            st.session_state["sentiment"] = (polarity, tone)

    st.subheader("🔍 Sentiment Analysis and Tone Detection")
    polarity, tone = st.session_state["sentiment"]
    st.write(f"**Tone:** {tone}")

    # Display Sentiment Gauge
    fig = create_gauge(polarity, tone)
    st.plotly_chart(fig, use_container_width=True)

    # Summarization Section
    if st.session_state["summary"] is None:
        with st.spinner("🧠 Summarizing... Hang tight!"):
            st.session_state["summary"] = summarize_long_text_cohere(st.session_state["preprocessed_text"])

    st.subheader("🔗 Summary")
    st.write(st.session_state["summary"])

# Question Answering Section
if st.session_state["preprocessed_text"]:
    st.subheader("❓ Ask a Question")
    question = st.text_input("Type your question below:")

    if question:
        st.session_state["current_question"] = question
        with st.spinner("🤔 Thinking..."):
            st.session_state["current_answer"] = answer_question_with_cohere(
                st.session_state["preprocessed_text"], question
            )
            # Save to history automatically
            st.session_state["qa_history"].append(
                (st.session_state["current_question"], st.session_state["current_answer"])
            )

    # Display Current Question and Answer
    if st.session_state["current_question"] and st.session_state["current_answer"]:
        st.markdown(f"<strong>Q:</strong> {st.session_state['current_question']}", unsafe_allow_html=True)
        st.markdown(f"<strong>A:</strong> {st.session_state['current_answer']}", unsafe_allow_html=True)

    # Q&A History Section
    st.subheader("📚 Q&A History")
    if st.session_state["qa_history"]:
        for i, (q, a) in enumerate(st.session_state["qa_history"], 1):
            st.write(f"**Q{i}:** {q}")
            st.write(f"**A{i}:** {a}")
            st.markdown("---")
    else:
        st.write("No questions asked yet.")

    if st.button("Clear Q&A History"):
        st.session_state["qa_history"] = []
        st.session_state["current_question"] = None
        st.session_state["current_answer"] = None

# Footer Section
st.markdown('<div class="footer">🚀 Built with ❤️ by Team Supernova</div>', unsafe_allow_html=True)
