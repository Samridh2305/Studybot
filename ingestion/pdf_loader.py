import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from common.config import settings
from utils.rag_service import get_file_hash


def load_and_split(file_path):
    all_documents = []

    file_name = os.path.basename(file_path)
    file_hash = get_file_hash(file_path)

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    total_pages = len(documents)

    for page_num, doc in enumerate(documents, start=1):
        doc.metadata.update({
            "source": file_name,
            "file_path": file_path,
            "file_hash": file_hash,
            "page": page_num,
            "total_pages": total_pages
        })
        all_documents.append(doc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    split_docs = splitter.split_documents(all_documents)

    for i, doc in enumerate(split_docs, start=1):
        doc.metadata["chunk_index"] = i
        doc.metadata["chunk_size"] = len(doc.page_content)

    return split_docs