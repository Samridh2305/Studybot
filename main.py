import hashlib
import os

from common.config import settings
from ingestion.pdf_loader import load_and_split
from llm.openai_client import get_answer
from storage.vectorstore.chroma_db import create_db, load_db
from utils.prompt import build_prompt


def generate_id(doc):
    text = doc.page_content
    source = doc.metadata.get("source", "")
    page= str(doc.metadata.get("page", ""))
    return hashlib.md5((text + source+page).encode()).hexdigest()


if os.path.exists("chroma_db"):
    print("Loading existing ChromaDB...\n")
    db = load_db()

    print("Adding documents (deduplicated)...\n")
    docs = load_and_split()

    ids = [generate_id(doc) for doc in docs]

    db.add_documents(docs, ids=ids)

else:
    print("Creating new ChromaDB...\n")
    docs = load_and_split()

    ids = [generate_id(doc) for doc in docs]

    db = create_db(docs)
    db.add_documents(docs, ids=ids)

print("Study Assistant Chatbot Ready! (type 'exit' to quit)\n")

while True:
    query = input("You: ")

    if query.lower() == "exit":
        break

    relevant_docs = db.similarity_search(query, k=settings.TOP_K)

    if not relevant_docs:
        print("\nBot: I couldn't find relevant information in the document.")
        continue

    sources={}

    for doc in relevant_docs:
        src=doc.metadata.get("source", "")
        page = doc.metadata.get("page", "")

        if src not in sources:
            sources[src]=set()

        sources[src].add(page)

    context = "\n\n".join([
        f"[{doc.metadata.get('source')} - page {doc.metadata.get('page')}]\n{doc.page_content}"
        for doc in relevant_docs
    ])

    prompt = build_prompt(context, query)

    answer = get_answer(prompt)

    if not answer or answer.strip() == "":
        answer = "I couldn't generate a proper answer. Try rephrasing your question."

    print("\nBot:", answer)
    print("-" * 50)
    print("\nSources:")
    for src, pages in sources.items():
        pages_str = ", ".join(str(p) for p in sorted(pages))
        print(f"- {src} (pages: {pages_str})")