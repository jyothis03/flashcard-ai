import { useState, useEffect } from "react"
import UploadSection from "./components/UploadSection"
import LoadingState from "./components/LoadingState"
import FlashcardDeck from "./components/FlashcardDeck"
import "./App.css"

const API_BASE = "http://localhost:8000"

function App() {
  const [stage, setStage] = useState("upload")
  const [jobId, setJobId] = useState(null)
  const [cards, setCards] = useState([])
  const [error, setError] = useState(null)

  function resetApp() {
    setStage("upload")
    setJobId(null)
    setCards([])
    setError(null)
  }

  async function handleUpload(file) {
    setError(null)
    setStage("loading")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.detail || "Upload failed")
      }

      const data = await response.json()
      setJobId(data.job_id)
    } catch (err) {
      setError(err.message)
      setStage("upload")
    }
  }

  useEffect(() => {
    if (!jobId) return

    const interval = setInterval(async () => {
      try {
        const response = await fetch(`${API_BASE}/status/${jobId}`)
        const data = await response.json()

        if (data.status === "done") {
          clearInterval(interval)
          setCards(data.result.cards)
          setStage("results")
        }

        if (data.status === "error") {
          clearInterval(interval)
          setError(data.detail || "Something went wrong")
          setStage("upload")
        }
      } catch (err) {
        clearInterval(interval)
        setError("Could not reach the server")
        setStage("upload")
      }
    }, 2000)

    return () => clearInterval(interval)
  }, [jobId])

  return (
    <div className="app">
      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}
      {stage === "upload" && <UploadSection onUpload={handleUpload} />}
      {stage === "loading" && <LoadingState />}
      {stage === "results" && <FlashcardDeck cards={cards} onReset={resetApp} />}
    </div>
  )
}

export default App