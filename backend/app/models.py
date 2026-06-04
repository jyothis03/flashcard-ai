from pydantic import BaseModel
from typing import Optional

class Flashcard(BaseModel):
    card_front: str
    card_back: str

class FlashcardDeck(BaseModel):
    cards: list[Flashcard]
    total_cards: int
    source_filename: str

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str

class StatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[FlashcardDeck] = None
    detail: Optional[str] = None 