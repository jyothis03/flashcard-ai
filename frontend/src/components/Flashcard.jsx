import { useState } from "react"
import "./Flashcard.css"

function Flashcard({ card_front, card_back }) {
  const [isFlipped, setIsFlipped] = useState(false)

  return (
    <div
      className="card-container"
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div className={`card-inner ${isFlipped ? "flipped" : ""}`}>
        <div className="card-face card-front">
          <span className="card-label">Question</span>
          <p className="card-text">{card_front}</p>
          <span className="card-hint">tap to flip</span>
        </div>
        <div className="card-face card-back">
          <span className="card-label card-label-answer">Answer</span>
          <p className="card-text">{card_back}</p>
          <span className="card-hint card-hint-back">tap to flip</span>
        </div>
      </div>
    </div>
  )
}

export default Flashcard