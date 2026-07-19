import type { WeakClass } from '@/services/api'

interface WeakClassesListProps {
  data: Record<string, WeakClass>
}

function WeakClassesList({ data }: WeakClassesListProps) {
  const entries = Object.entries(data)

  if (entries.length === 0) {
    return <p className="text-sm text-ink-soft">No weak classes detected.</p>
  }

  return (
    <ul className="space-y-2">
      {entries.map(([className, metrics]) => (
        <li
          key={className}
          className="rounded-lg border border-warning/40 bg-warning-soft px-3 py-2 text-sm"
        >
          <span className="font-mono text-warning">{className}</span>
          <span className="ml-2 text-ink-soft">
            {(metrics.recall * 100).toFixed(2)}% recall &middot; {metrics.support.toLocaleString()}{' '}
            support
          </span>
        </li>
      ))}
    </ul>
  )
}

export default WeakClassesList
