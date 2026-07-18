interface LoadingSpinnerProps {
  label?: string
}

/**
 * Small reusable loading indicator. Unlike the section components this
 * is fully functional already (not a placeholder) - there's no data
 * shape to wait on, just drop it into any section once that section
 * starts an async request in a later phase.
 */
function LoadingSpinner({ label = 'Loading…' }: LoadingSpinnerProps) {
  return (
    <div className="flex items-center justify-center gap-3 py-10 text-ink-soft">
      <span
        className="h-5 w-5 animate-spin rounded-full border-2 border-border border-t-signal"
        aria-hidden="true"
      />
      <span className="font-mono text-xs uppercase tracking-widest">{label}</span>
    </div>
  )
}

export default LoadingSpinner
