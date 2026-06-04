import { useState, useRef } from "react"
import "./UploadSection.css"

function UploadSection({ onUpload }) {
  const [isDragging, setIsDragging] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const inputRef = useRef(null)

  function handleFile(file) {
    if (!file) return
    setSelectedFile(file)
    onUpload(file)
  }

  function handleDrop(e) {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  function handleDragOver(e) {
    e.preventDefault()
    setIsDragging(true)
  }

  function handleDragLeave(e) {
    e.preventDefault()
    setIsDragging(false)
  }

  return (
    <div className="upload-page">
      <div className="orb orb-1" />
      <div className="orb orb-2" />

      <div className="upload-content">
        <header className="upload-header">
          <div className="upload-badge">AI — Powered</div>
          <h1 className="upload-title">
            Turn any PDF into<br />
            <em>beautiful flashcards for quick revisions!</em>
          </h1>
          <p className="upload-subtitle">
            Drop your notes, textbooks, or documents.
            Walk away with a full study deck.
          </p>
        </header>

        <div
          className={`upload-zone ${isDragging ? "dragging" : ""}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            onChange={e => handleFile(e.target.files[0])}
            style={{ display: "none" }}
          />
          <div className="upload-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 15V3" />
              <path d="M7 8l5-5 5 5" />
              <path d="M20 15v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4" />
            </svg>
          </div>
          <p className="upload-zone-main">
            {selectedFile ? selectedFile.name : "Drop your PDF here"}
          </p>
          <span className="upload-zone-sub">
            {selectedFile
              ? "Starting generation..."
              : "or click to browse · PDF only · Max 10MB"}
          </span>
        </div>

        <div className="upload-features">
          <div className="feature"><span className="feature-dot" />For Quick Revision</div>
          <div className="feature"><span className="feature-dot" />AI-generated Q&amp;A</div>
          <div className="feature"><span className="feature-dot" />Instant flip cards</div>
        </div>
      </div>
    </div>
  )
}

export default UploadSection