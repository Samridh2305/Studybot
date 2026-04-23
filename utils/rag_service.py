import hashlib
import os

from common.config import settings
from llm.openai_client import get_answer
from storage.vectorstore.chroma_db import (
    create_db,
    load_db
)
from utils.prompt import build_prompt


def generate_id(doc):
    text = doc.page_content
    file_hash = doc.metadata.get("file_hash", "")
    page = str(doc.metadata.get("page", ""))
    raw= text+file_hash+page
    return hashlib.md5(raw.encode()).hexdigest()

def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def init_db():
    if os.path.exists("chroma_db"):
        print("Loading existing ChromaDB...\n")
        db = load_db()
    else:
        print("Creating new ChromaDB...\n")
        db=create_db()
    return db


def answer_query(db, query: str):
    relevant_docs = db.similarity_search(query, k=settings.TOP_K)

    if not relevant_docs:
        return {
            "answer": "No relevant information found.",
            "sources": {}
        }
    sources = {}

    for doc in relevant_docs:
        src = doc.metadata.get("source", "")
        page = doc.metadata.get("page", "")

        if src not in sources:
            sources[src] = set()

        sources[src].add(page)

    context = "\n\n".join([
        f"[{doc.metadata.get('source')} - page {doc.metadata.get('page')}]\n{doc.page_content}"
        for doc in relevant_docs
    ])

    prompt = build_prompt(context, query)
    answer = get_answer(prompt)

    if not answer or answer.strip() == "":
        answer = "I couldn't generate a proper answer."
    return {
        "answer": answer,
        "sources": {
            src: sorted(list(pages)) for src, pages in sources.items()
        }
    }
