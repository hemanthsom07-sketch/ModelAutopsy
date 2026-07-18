import type { ReactNode } from 'react'

interface ChartPanelProps {
  title: string
  isEmpty: boolean
  emptyMessage?: string
  children: ReactNode
}

/**
 * Shared wrapper for every individual chart inside the Charts section.
 * Gives every chart a consistent title, fixed height (Recharts'
 * ResponsiveContainer needs a real pixel height from its parent to size
 * against), and a graceful empty state instead of an empty plot area.
 */
function ChartPanel({ title, isEmpty, emptyMessage = 'No data available', children }: ChartPanelProps) {
  return (
    <div className="rounded-lg border border-border bg-canvas/40 p-4">
      <p className="mb-3 truncate font-mono text-[11px] uppercase tracking-widest text-ink-faint">
        {title}
      </p>
      {isEmpty ? (
        <div className="flex h-48 items-center justify-center text-center text-xs text-ink-faint">
          {emptyMessage}
        </div>
      ) : (
        <div className="h-48">{children}</div>
      )}
    </div>
  )
}

export default ChartPanel
