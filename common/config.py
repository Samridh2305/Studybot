import os
from typing import List

from dotenv import load_dotenv

load_dotenv()

class Settings:
    # LLM Configurations
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Document Chunking Configurations
    UPLOAD_DIR = os.getenv("UPLOAD_DIR")

    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
    TOP_K = int(os.getenv("TOP_K"))
    PERSIST_DIR = os.getenv("PERSIST_DIR", "chroma_db")
    COLLECTION = os.getenv("COLLECTION")

    CORS_ALLOW_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True

settings=Settings()


