import Card from '@/components/Card'

interface InsightsProps {
  data: string[] | null
}

/** Renders the deterministic `insights` sentence list from POST /analyze. */
function Insights({ data }: InsightsProps) {
  if (!data) {
    return <Card eyebrow="Findings" title="Insights" />
  }

  return (
    <Card eyebrow="Findings" title="Insights" status="Ready">
      {data.length === 0 ? (
        <p className="text-sm text-ink-soft">No insights were generated for this dataset.</p>
      ) : (
        <ul className="space-y-2">
          {data.map((insight, index) => (
            <li key={index} className="flex gap-2 text-sm text-ink-soft">
              <span
                className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-signal"
                aria-hidden="true"
              />
              <span>{insight}</span>
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}

export default Insights
