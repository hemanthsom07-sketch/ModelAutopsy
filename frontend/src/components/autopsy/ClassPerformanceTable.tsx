import type { ClassPerformanceEntry, ClassPerformanceMetrics } from '@/services/api'

interface ClassPerformanceTableProps {
  data: Record<string, ClassPerformanceEntry>
}

function isMetricsObject(value: ClassPerformanceEntry): value is ClassPerformanceMetrics {
  return typeof value === 'object' && value !== null
}

/**
 * class_performance (from sklearn's classification_report) mixes
 * per-class metric objects with a bare "accuracy" number under the same
 * dict. The bare number is skipped here - not omitted from the
 * response, just not shown as a broken row in a table meant for
 * per-class-shaped rows, since the same accuracy value is already shown
 * in the stat strip above.
 */
function ClassPerformanceTable({ data }: ClassPerformanceTableProps) {
  const rows = Object.entries(data).filter(
    (entry): entry is [string, ClassPerformanceMetrics] => isMetricsObject(entry[1]),
  )

  if (rows.length === 0) {
    return <p className="text-sm text-ink-soft">No class performance data available.</p>
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-border">
      <table className="w-full text-left text-sm">
        <thead>
          <tr className="border-b border-border bg-canvas/40 font-mono text-[11px] uppercase tracking-widest text-ink-faint">
            <th className="px-3 py-2">Class</th>
            <th className="px-3 py-2">Precision</th>
            <th className="px-3 py-2">Recall</th>
            <th className="px-3 py-2">F1</th>
            <th className="px-3 py-2">Support</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([className, metrics]) => (
            <tr key={className} className="border-b border-border last:border-0">
              <td className="px-3 py-2 text-ink-soft">{className}</td>
              <td className="px-3 py-2 font-mono text-ink">
                {(metrics.precision * 100).toFixed(2)}%
              </td>
              <td className="px-3 py-2 font-mono text-ink">{(metrics.recall * 100).toFixed(2)}%</td>
              <td className="px-3 py-2 font-mono text-ink">
                {(metrics['f1-score'] * 100).toFixed(2)}%
              </td>
              <td className="px-3 py-2 font-mono text-ink">{metrics.support.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default ClassPerformanceTable
