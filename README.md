# AI-Powered Flashcard Generator

A full-stack application that transforms dense PDF documents into bite-sized, study-ready flashcards using Google's Gemini Flash LLM.

## 🚀 Project Overview
This project was built as a deep dive into building production-ready AI integrations. It focuses on handling long-running tasks asynchronously to ensure a smooth user experience.

### Key Features
- **PDF Extraction:** Parses text from uploaded PDF documents using PyMuPDF.
- **Intelligent Chunking:** Segments large documents into manageable parts for LLM processing.
- **Asynchronous Orchestration:** Uses a polling-based background task architecture to process files without blocking the UI.
- **AI Flashcard Generation:** Leverages `gemini-flash-latest` with structured JSON output and custom retry logic for high reliability.
- **Modern React UI:** A sleek, responsive interface with interactive flip cards.

## 🛠️ Technical Deep Dive (What I Learned)
- **Backend Design:** Implemented a "Job/Status" pattern using FastAPI's `BackgroundTasks`. While using an in-memory store for this iteration, the architecture is decoupled to easily support Redis/Celery for distributed processing.
- **LLM Resiliency:** Developed a custom retry mechanism with exponential backoff to handle transient API issues (Rate Limits, 503s) and non-deterministic JSON responses.
- **Data Integrity:** Used Pydantic for strict schema validation of LLM responses, ensuring the frontend never receives malformed data.
- **State Management:** Managed complex frontend states to handle the lifecycle of an upload—from "Processing" to "Results"—via polling.

## 📦 Tech Stack
- **Backend:** FastAPI, Python, Google GenAI SDK, PyMuPDF.
- **Frontend:** React, Vite, CSS3.
- **AI Model:** Google Gemini Flash.

## ⚙️ Setup & Installation

1. **Clone the repository**
2. **Backend Setup:**
   - Navigate to `/backend`.
   - Create a `.env` file and add your `GEMINI_API_KEY`.
   - Install dependencies: `pip install -r requirements.txt`.
   - Start the server: `uvicorn main:app --reload`.
3. **Frontend Setup:**
   - Navigate to `/frontend`.
   - Install dependencies: `npm install`.
   - Start the development server: `npm run dev`.

## 🔮 Future Roadmap
- Integrate Redis/Celery for better scalability.
- Add persistent storage (PostgreSQL) for deck history.
- Support OCR for scanned PDF images.
