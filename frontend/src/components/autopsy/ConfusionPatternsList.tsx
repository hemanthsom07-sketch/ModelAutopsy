interface ConfusionPatternsListProps {
  data: Record<string, number>
}

function ConfusionPatternsList({ data }: ConfusionPatternsListProps) {
  const entries = Object.entries(data)

  if (entries.length === 0) {
    return <p className="text-sm text-ink-soft">No confusion patterns to show.</p>
  }

  return (
    <ul className="space-y-2">
      {entries.map(([pattern, count]) => (
        <li
          key={pattern}
          className="flex items-center justify-between rounded-lg border border-border bg-canvas/40 px-3 py-2 text-sm"
        >
          <span className="font-mono text-ink-soft">{pattern}</span>
          <span className="font-mono text-ink">{count.toLocaleString()}</span>
        </li>
      ))}
    </ul>
  )
}

export default ConfusionPatternsList
