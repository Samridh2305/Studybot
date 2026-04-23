# Study Assistant Chatbot (RAG-based)
Study Assistant Chatbot (RAG-based)

## Features
1. Multi-PDF ingestion from a directory
2. Intelligent text chunking with overlap
3. Semantic search using vector embeddings
4. Metadata tracking (file name, page number, chunk ID)
5. Deduplication using hashing
6. LLM-powered answers (OpenAI)
7. Source citations with page references
8. Fast retrieval using Chroma vector database

## Flow

```
PDFs
 ↓
Load & Split (pages → chunks)
 ↓
Add Metadata (source, page, chunk_id)
 ↓
Generate Embeddings
 ↓
Store in Chroma DB
 ↓
User Query
 ↓
Similarity Search
 ↓
Top Relevant Chunks
 ↓
Build Context
 ↓
LLM Generates Answer
 ↓
Display Answer + Sources
```

### Project Structure
```
.
├── ingestion/
│   └── pdf_loader.py        # Load and split PDFs into chunks
├── storage/
│   └── vectorstore/
│       └── chroma_db.py     # Create/load Chroma DB
├── embeddings/
│   └── embedder.py          # Embedding model setup
├── llm/
│   └── openai_client.py     # LLM API interaction
├── utils/
│   └── prompt.py            # Prompt construction
├── common/
│   └── config.py            # Configuration settings
├── data/                    # Folder containing PDFs
├── chroma_db/               # Persisted vector database
├── main.py                  # Entry point
└── README.md
```

### Installing
* Clone the repo

```
git clone https://github.com/your-username/study-assistant.git
cd study-assistant
```

*Create Virtual Environment

```
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

*Install dependencies

```
pip install -r requirements.txt
```

*Variables in Env File

```
OPENAI_API_KEY
TOP_K
CHUNK_OVERLAP
CHUNK_SIZE
COLLECTION
PERSIST_DIR
UPLOAD_DIR
```

1. Enter Query related to uploaded document
2. Example Output

```
Bot: Python is a high-level programming language widely used in AI.

Sources:
- notes.pdf (pages: 2, 3)
- ai_book.pdf (page 5)
```


