import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BACKEND_DIR / ".env")


PRODUCTS_FILE = BACKEND_DIR / "data" / "products.json"
CHROMA_DIR = BACKEND_DIR / "chroma_db"

COLLECTION_NAME = "products"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
GROQ_BASE_URL = os.getenv(
    "GROQ_BASE_URL",
    "https://api.groq.com/openai/v1",
)

LLM_TEMPERATURE = 0.3