import type { DominantFailure } from '@/services/api'

interface DominantFailureCardProps {
  data: DominantFailure
}

function DominantFailureCard({ data }: DominantFailureCardProps) {
  return (
    <div className="rounded-lg border border-critical/40 bg-critical-soft p-4">
      <p className="font-mono text-[11px] uppercase tracking-widest text-ink-faint">
        Dominant failure pattern
      </p>
      <p className="mt-2 font-display text-lg text-ink">
        <span className="font-mono text-critical">{data.actual_class}</span>
        {' \u2192 '}
        <span className="font-mono text-critical">{data.predicted_class}</span>
      </p>
      <p className="mt-1 text-sm text-ink-soft">
        {data.count.toLocaleString()} cases &middot; {data.percentage_of_errors.toFixed(2)}% of all
        errors
      </p>
    </div>
  )
}

export default DominantFailureCard
