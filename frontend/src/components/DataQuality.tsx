import Card from '@/components/Card'
import type { DataQuality as DataQualityData } from '@/services/api'

interface DataQualityProps {
  data: DataQualityData | null
}

/** Renders the data_quality warning list from POST /analyze. */
function DataQuality({ data }: DataQualityProps) {
  if (!data) {
    return <Card eyebrow="Diagnostics" title="Data Quality" />
  }

  return (
    <Card eyebrow="Diagnostics" title="Data Quality" status="Ready">
      {data.warnings.length === 0 ? (
        <p className="text-sm text-ink-soft">No data quality issues were detected.</p>
      ) : (
        <ul className="space-y-2">
          {data.warnings.map((warning, index) => (
            <li
              key={index}
              className="rounded-lg border border-border bg-canvas/40 px-3 py-2 text-sm text-ink-soft"
            >
              {warning}
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}

export default DataQuality
