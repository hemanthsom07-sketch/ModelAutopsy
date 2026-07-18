import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import ChartPanel from '@/components/charts/ChartPanel'
import type { MissingValuesChartData } from '@/services/api'

interface MissingValuesChartProps {
  data: MissingValuesChartData
}

/** Single bar chart of missing-value counts across every column. */
function MissingValuesChart({ data }: MissingValuesChartProps) {
  const series = data.columns.map((column, index) => ({
    column,
    missing: data.missing_counts[index],
  }))
  const isEmpty = series.every((item) => item.missing === 0)

  return (
    <ChartPanel
      title="Missing values by column"
      isEmpty={isEmpty}
      emptyMessage="No missing values in this dataset"
    >
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={series} margin={{ top: 4, right: 8, left: -16, bottom: 24 }}>
          <XAxis
            dataKey="column"
            tick={{ fontSize: 9, fill: 'var(--color-ink-faint)' }}
            angle={-35}
            textAnchor="end"
            interval={0}
            height={50}
          />
          <YAxis tick={{ fontSize: 10, fill: 'var(--color-ink-faint)' }} allowDecimals={false} />
          <Tooltip
            contentStyle={{
              background: 'var(--color-surface)',
              border: '1px solid var(--color-border)',
              borderRadius: 8,
              fontSize: 12,
            }}
            labelStyle={{ color: 'var(--color-ink)' }}
          />
          <Bar dataKey="missing" fill="var(--color-warning)" radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartPanel>
  )
}

export default MissingValuesChart
