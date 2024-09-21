# app/grader.py
import re
from typing import Optional
import google.generativeai as genai
from .config import settings

# Configure the API key
genai.configure(api_key=settings.GEMINI_API_KEY)

# Define safety settings and generation configuration
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Initialize chat session
chat_session = model.start_chat(history=[])

def check_essay(task: str, essay: str) -> str:
    """
    Check the essay for spelling or grammar.
    """
    message = f"{task} the following essay:\n\n{essay}"
    response = chat_session.send_message(message)
    return response.text.strip()

def grade_essay(title: str, essay: str) -> dict:
    """
    Grade the essay and provide feedback.
    """
    message = (
        f"Title: {title}\n\n{essay}\n\n"
        "Please provide a grade band (0.0 - 9.0) for this IELTS essay. "
        "The response should include the phrase 'Grade Band: X.X'. "
        "Also, provide detailed feedback based on task response, coherence and cohesion, "
        "lexical resource, and grammatical range."
    )
    response = chat_session.send_message(message)
    feedback = response.text.strip()

    # Extract grade band using regex
    grade_match = re.search(
        r'(?:grade\s*band|score|rating)[:\s]*(\d+(\.\d+)?)',
        feedback,
        re.IGNORECASE
    )
    if not grade_match:
        grade_match = re.search(
            r'(\d+(\.\d+)?)/9|(\d+(\.\d+)?)\s*out of 9',
            feedback,
            re.IGNORECASE
        )
    grade_band = float(grade_match.group(1)) if grade_match else None

    # Word count
    word_count = len(essay.split())
    warning = None
    if word_count < 250:
        warning = 'Your essay is below the recommended minimum word count for IELTS (250 words).'

    return {
        "feedback": feedback,
        "grade_band": grade_band,
        "word_count": word_count,
        "warning": warning
    }
