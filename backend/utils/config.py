"""Environment parsing configurations layer. Loads properties from .env records."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# LLM Keys
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Processing Parameters
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "400"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
MIN_MESSAGES_FOR_ANALYSIS = int(os.getenv("MIN_MESSAGES", "20"))
MAX_SAMPLE_MESSAGES = int(os.getenv("MAX_SAMPLE", "100"))

# Privacy Guards
ANONYMIZE_NAMES = os.getenv("ANONYMIZE_NAMES", "true").lower() == "true"
STORE_RAW_MESSAGES = os.getenv("STORE_RAW", "false").lower() == "true"
