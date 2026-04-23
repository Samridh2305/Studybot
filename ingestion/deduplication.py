from ingestion.pdf_loader import load_and_split
from utils.rag_service import (
    generate_id,
    get_file_hash
)


def file_exists(db, file_hash):
    results = db.get(where={"file_hash": file_hash})
    return len(results["ids"]) > 0


def ingest_file(db, file_path):
    file_hash = get_file_hash(file_path)

    if file_exists(db, file_hash):
        print("File already exists in DB. Skipping.")
        return

    docs = load_and_split(file_path)

    ids = [generate_id(doc) for doc in docs]

    existing = db.get(ids=ids)
    existing_ids = set(existing["ids"])

    new_docs = []
    new_ids = []

    for doc, id_ in zip(docs, ids):
        if id_ not in existing_ids:
            new_docs.append(doc)
            new_ids.append(id_)

    if new_docs:
        db.add_documents(new_docs, ids=new_ids)
        print("File ingested successfully.")
    else:
        print("All chunks already exist in DB.")