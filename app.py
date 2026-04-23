import uuid

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    BackgroundTasks
)
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from common.config import settings
from ingestion.polling import ingest_file_with_status, task_status
from utils.rag_service import (
    init_db,
    answer_query
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing DB...")
    app.state.db = init_db()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(request: QueryRequest):
    db = app.state.db
    return answer_query(db, request.question)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files allowed"}

    job_id = str(uuid.uuid4())

    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)
    db = app.state.db
    background_tasks.add_task(
        ingest_file_with_status,
        db,
        file_path,
        job_id
    )

    return {
        "job_id": job_id,
        "status": "processing"
    }

@app.get("/status")
def check_status(job_id:str):
    status=task_status.get(job_id,"not_found")
    return {"job_id": job_id, "status": status}