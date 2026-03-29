import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from common.config import settings

def load_and_split():
    all_documents = []

    for file in os.listdir(settings.PDF_DIR):
        if file.endswith(".pdf"):
            file_path = os.path.join(settings.PDF_DIR, file)

            loader = PyPDFLoader(file_path)
            documents = loader.load()

            for doc in documents:
                doc.metadata["source"] = file
                all_documents.append(doc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    return splitter.split_documents(all_documents)