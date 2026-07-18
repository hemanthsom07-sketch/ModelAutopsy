/**
 * Persistent top navigation. Static content only for Phase 4A - no
 * links or actions yet.
 */
function Navbar() {
  return (
    <header className="sticky top-0 z-10 border-b border-border bg-canvas/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center gap-3 px-6 py-4">
        <span className="h-2 w-2 shrink-0 rounded-full bg-signal" aria-hidden="true" />
        <div>
          <h1 className="font-display text-lg font-semibold tracking-tight text-ink">
            ModelAutopsy
          </h1>
          <p className="text-xs text-ink-soft">
            AI Dataset Analysis &amp; Model Failure Explanation Platform
          </p>
        </div>
      </div>
    </header>
  )
}

export default Navbar
