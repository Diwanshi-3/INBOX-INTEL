"""NLP preprocessing module for email text."""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
def ensure_nltk_data():
    """Download NLTK data if not present."""
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt", quiet=True)
    
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt_tab", quiet=True)
    
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords", quiet=True)


ensure_nltk_data()

STOP_WORDS = set(stopwords.words("english"))


def preprocess_text(text: str) -> str:
    """
    Preprocess email text for spam detection.
    
    Steps:
    1. Lowercase conversion
    2. Remove URLs
    3. Remove email addresses
    4. Remove punctuation
    5. Remove numbers
    6. Remove stopwords
    7. Remove extra whitespace
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", " ", text)
    
    # Remove email addresses
    text = re.sub(r"\S+@\S+", " ", text)
    
    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Remove numbers
    text = re.sub(r"\d+", " ", text)
    
    # Tokenize and remove stopwords
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    
    tokens = [token for token in tokens if token not in STOP_WORDS and len(token) > 2]
    
    # Rejoin
    text = " ".join(tokens)
    
    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()
    
    return text


def prepare_email_text(subject: str, body: str) -> str:
    """Combine and preprocess subject and body."""
    combined = f"{subject} {body}"
    return preprocess_text(combined)
