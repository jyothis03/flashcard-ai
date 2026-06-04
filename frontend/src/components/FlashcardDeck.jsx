import Flashcard from "./Flashcard"
import "./FlashcardDeck.css"

function FlashcardDeck({ cards, onReset }) {
  return (
    <div className="deck-page">
      <header className="deck-header">
        <button className="deck-back-btn" onClick={onReset}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M19 12H5M12 5l-7 7 7 7" />
          </svg>
          New PDF
        </button>

        <div className="deck-header-center">
          <h2 className="deck-title">Your <em>Flashcards</em></h2>
          <span className="deck-count">{cards.length} cards generated</span>
        </div>

        <div className="deck-header-spacer" />
      </header>

      <p className="deck-hint">Click any card to reveal the answer</p>

      <div className="deck-grid">
        {cards.map((card, index) => (
          <Flashcard
            key={index}
            card_front={card.card_front}
            card_back={card.card_back}
          />
        ))}
      </div>
    </div>
  )
}

export default FlashcardDeck