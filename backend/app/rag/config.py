import os
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BACKEND_DIR / ".env")


PRODUCTS_FILE = BACKEND_DIR / "data" / "products.json"
CHROMA_DIR = BACKEND_DIR / "chroma_db"

COLLECTION_NAME = "products"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

LLM_TEMPERATURE = 0.3