interface ErrorMessageProps {
  message: string
  /** Optional extra detail - mirrors backend/schemas/responses.py ErrorResponse{error, detail} */
  detail?: string
}

/**
 * Reusable error banner. Fully functional already (not a placeholder) -
 * its shape mirrors the backend's ErrorResponse so it can display any
 * API error unchanged once error handling is wired up in a later phase.
 */
function ErrorMessage({ message, detail }: ErrorMessageProps) {
  return (
    <div className="rounded-xl border border-critical/40 bg-critical-soft px-4 py-3 text-sm">
      <p className="font-medium text-critical">{message}</p>
      {detail && <p className="mt-1 text-ink-soft">{detail}</p>}
    </div>
  )
}

export default ErrorMessage
