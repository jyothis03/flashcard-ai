import os
import json
import time
from google import genai
from dotenv import load_dotenv
from pydantic import ValidationError
from app.models import Flashcard

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

RETRYABLE_STATUS_CODES = { 503,429,500 } 
MAX_RETRIES  = 3
BASE_WAIT = 2

def generate_flashcards_from_chunk(chunk: str) -> list[Flashcard]:
    prompt = f"""
You are a flashcard generator. Your job is to read the text below and create flashcards from it.

STRICT RULES:
- Respond ONLY with a valid JSON array.
- Do not write anything before or after the JSON array.
- Do not use markdown, code blocks, or backticks.
- Each item in the array must have exactly two fields: "card_front" and "card_back".
- "card_front" is the question or concept.
- "card_back" is the answer or explanation.
- Exhaustively cover the technical details. Generate between 6 and 10 flashcards for this specific text.

EXAMPLE OUTPUT FORMAT:
[
  {{"card_front": "What is photosynthesis?", "card_back": "The process by which plants convert sunlight into energy"}},
  {{"card_front": "What molecule carries oxygen in blood?", "card_back": "Hemoglobin"}}
]

TEXT TO CONVERT:
{chunk}
"""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )

            if not response.text:
                print("AI Error: The response was empty or blocked by safety filters.")
                return []

            raw_text = response.text.strip()
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()

            parsed = json.loads(raw_text)
            return [Flashcard(**item) for item in parsed]

        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Attempt {attempt + 1}: Failed to parse AI response: {e}")
            last_error = e
        except Exception as e:
            last_error = e
            error_code = getattr(e, "code", None) or getattr(e, "status_code", None)

            if error_code not in RETRYABLE_STATUS_CODES:
                print(f"Permanent error: {e}")
                break
            
            wait_time = BASE_WAIT ** (attempt + 1)
            print(f"Transient error on attempt {attempt + 1}, retrying in {wait_time}s: {e}")
            time.sleep(wait_time)

    print(f"All {MAX_RETRIES} attempts failed. Last error: {last_error}")
    return []