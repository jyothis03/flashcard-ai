import uuid
from pydantic import ValidationError
from app.models import FlashcardDeck
from app.pdf_processing import extract_text_from_pdf, chunk_text
from app.ai import generate_flashcards_from_chunk

jobs: dict = {}

def create_job()->str:
    job_id=str(uuid.uuid4())
    jobs[job_id]={"status":"processing"}
    return job_id

def process_pdf(job_id:str, file_bytes: bytes, filename: str):
    
    try:
        text = extract_text_from_pdf(file_bytes)
        if not text.strip():
            jobs[job_id] = {
                "status": "error",
                "detail": "Could not extract text. PDF may be scanned or image-based."
            }
            return

        chunks = chunk_text(text)
        print(f"DEBUG: Document split into {len(chunks)} chunks.")
        
        all_cards = []

        for chunk in chunks:
                cards = generate_flashcards_from_chunk(chunk)
                all_cards.extend(cards)

        if not all_cards:
            jobs[job_id] = {
                "status": "error",
                "detail": "Failed to generate flashcards from this document."
            }
            return

        deck = FlashcardDeck(
            cards=all_cards,
            total_cards=len(all_cards),
            source_filename=filename
        )

        jobs[job_id] = {"status": "done", "result": deck}
    
    except Exception as e:
        jobs[job_id] = {"status": "failed", "detail": str(e)}