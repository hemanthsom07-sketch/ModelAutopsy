import Card from '@/components/Card'
import type { DatasetSummary as DatasetSummaryData } from '@/services/api'

interface DatasetSummaryProps {
  data: DatasetSummaryData | null
}

function StatItem({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="rounded-lg border border-border bg-canvas/40 px-4 py-3">
      <p className="font-mono text-[11px] uppercase tracking-widest text-ink-faint">{label}</p>
      <p className="mt-1 font-mono text-xl text-ink">{value}</p>
    </div>
  )
}

/** Renders dataset_summary from POST /analyze as a row of stat readouts. */
function DatasetSummary({ data }: DatasetSummaryProps) {
  if (!data) {
    return <Card eyebrow="Overview" title="Dataset Summary" />
  }

  return (
    <Card eyebrow="Overview" title="Dataset Summary" status="Ready">
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
        <StatItem label="Rows" value={data.total_rows.toLocaleString()} />
        <StatItem label="Columns" value={data.total_columns} />
        <StatItem label="Numeric" value={data.numeric_columns} />
        <StatItem label="Categorical" value={data.categorical_columns} />
        <StatItem label="Missing" value={data.total_missing_values.toLocaleString()} />
        <StatItem label="Duplicates" value={data.duplicate_rows.toLocaleString()} />
      </div>

      {data.converted_numeric_columns.length > 0 && (
        <p className="mt-4 text-sm text-ink-soft">
          Converted to numeric:{' '}
          <span className="font-mono text-ink">
            {data.converted_numeric_columns.join(', ')}
          </span>
        </p>
      )}
    </Card>
  )
}

export default DatasetSummary
