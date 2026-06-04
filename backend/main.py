from fastapi import FastAPI
from app.routes import router
from app.ai import generate_flashcards_from_chunk
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(router)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    test_chunk = """
    Photosynthesis is the process by which green plants and some other organisms 
    use sunlight to synthesize nutrients from carbon dioxide and water. 
    It generates oxygen as a byproduct and is the foundation of most food chains on Earth.
    Chlorophyll, the green pigment in plant leaves, is responsible for absorbing light energy.
    """
    cards = generate_flashcards_from_chunk(test_chunk)
    for card in cards:
        print(f"Q: {card.card_front}")
        print(f"A: {card.card_back}")
        print()