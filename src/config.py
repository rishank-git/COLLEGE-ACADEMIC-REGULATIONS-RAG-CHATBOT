from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Paths
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

PDF_PATH = DATA_DIR / "regulations.pdf"
CHUNKS_PATH = DATABASE_DIR / "chunks.json"
CHROMA_PATH = DATABASE_DIR / "chroma"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Retrieval settings
TOP_K = 3

# Claude API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")                                                                                              