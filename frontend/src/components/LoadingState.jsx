import "./LoadingState.css"

function LoadingState() {
  return (
    <div className="loading-page">
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="loading-content">
        <div className="loading-ring">
          <div className="loading-ring-dot" />
        </div>
        <h2 className="loading-title">
          Crafting your<br /><em>flashcards</em>
        </h2>
        <p className="loading-text">Reading and analyzing your document</p>
        <div className="loading-dots">
          <span /><span /><span />
        </div>
      </div>
    </div>
  )
}

export default LoadingState