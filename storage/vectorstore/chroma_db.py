from langchain_chroma import Chroma

from common.config import settings
from embeddings.embedder import get_embeddings

def create_db(docs):
    embeddings = get_embeddings()

    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=settings.PERSIST_DIR,
        collection_name=settings.COLLECTION
    )
    return db

def load_db():
    embeddings = get_embeddings()

    return Chroma(
        persist_directory=settings.PERSIST_DIR,
        embedding_function=embeddings,
        collection_name=settings.COLLECTION
    )