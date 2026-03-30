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

            total_pages=len(documents)

            for page_num,doc in enumerate(documents, start=1):
                doc.metadata.update({
                    "source": file,
                    "file_path": file_path,
                    "page": page_num,
                    "total_pages": total_pages
                })
                all_documents.append(doc)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    split_docs= splitter.split_documents(all_documents)

    for chunk_id,doc in enumerate(split_docs, start=1):
        doc.metadata["chunk_id"] = chunk_id
        doc.metadata["chunk_size"] = len(doc.page_content)

    return split_docs