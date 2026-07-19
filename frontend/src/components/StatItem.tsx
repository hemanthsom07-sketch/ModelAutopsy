interface StatItemProps {
  label: string
  value: string | number
}

/**
 * Small labelled stat readout, used by PredictionResults and
 * AutopsyResults. DatasetSummary.tsx has its own local version of this
 * same pattern - left untouched rather than refactored to share this
 * one, since modifying it isn't permitted this phase.
 */
function StatItem({ label, value }: StatItemProps) {
  return (
    <div className="rounded-lg border border-border bg-canvas/40 px-4 py-3">
      <p className="font-mono text-[11px] uppercase tracking-widest text-ink-faint">{label}</p>
      <p className="mt-1 font-mono text-xl text-ink">{value}</p>
    </div>
  )
}

export default StatItem
