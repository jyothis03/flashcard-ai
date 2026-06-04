
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.models import FlashcardDeck, JobResponse, StatusResponse
from app.tasks import create_job, process_pdf, jobs


router = APIRouter()

MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/upload", response_model=JobResponse)
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...) ):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted"
        )

    file_bytes = await file.read()

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE_MB}MB."
        )

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    job_id= create_job()
    background_tasks.add_task(process_pdf, job_id, file_bytes, file.filename)

    return JobResponse(
        job_id=job_id,
        status="processing",
        message="File received. Flashcards are being generated."
    )

@router.get("/status/{job_id}", response_model=StatusResponse)
async def get_status(job_id: str):
    job = jobs.get(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
    if job["status"] == "done":
        return StatusResponse(
            job_id=job_id,
            status="done",
            result=job["result"]
        )

    if job["status"] == "error":
        return StatusResponse(
            job_id=job_id,
            status="error",
            detail=job["detail"]
        )    

    return StatusResponse(
        job_id=job_id,
        status="processing"
    )