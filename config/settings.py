"""
Configuration settings for Article Scout
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src" / "article_scout"
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"

# Environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))

# PDF extraction settings
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "5000"))
MAX_INPUT_CHARS = int(os.getenv("MAX_INPUT_CHARS", "5000"))

# Streamlit settings
STREAMLIT_SERVER_PORT = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
STREAMLIT_SERVER_ADDRESS = os.getenv("STREAMLIT_SERVER_ADDRESS", "0.0.0.0")

# Validation
def validate_config():
    """Validate that required configuration is present"""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY not found in environment variables. "
            "Please ensure it is configured in your .env file"
        )
    
    if GROQ_API_KEY == "your_groq_api_key_here":
        raise ValueError(
            "Please set your actual GROQ_API_KEY in the .env file. "
            "Get your API key from: https://console.groq.com/"
        )
