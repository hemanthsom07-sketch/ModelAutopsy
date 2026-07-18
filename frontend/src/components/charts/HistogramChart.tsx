import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import ChartPanel from '@/components/charts/ChartPanel'
import type { HistogramData } from '@/services/api'

interface HistogramChartProps {
  column: string
  data: HistogramData
}

function formatBinLabel(start: number, end: number): string {
  const fmt = (value: number) => (Number.isInteger(value) ? value.toString() : value.toFixed(1))
  return start === end ? fmt(start) : `${fmt(start)}\u2013${fmt(end)}`
}

/** One bin/frequency bar chart per numeric column in chart_data.histograms. */
function HistogramChart({ column, data }: HistogramChartProps) {
  const isEmpty = data.bin_counts.length === 0
  const series = data.bin_counts.map((count, index) => ({
    label: formatBinLabel(data.bin_edges[index], data.bin_edges[index + 1]),
    count,
  }))

  return (
    <ChartPanel title={column} isEmpty={isEmpty} emptyMessage="No numeric values to plot">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={series} margin={{ top: 4, right: 8, left: -16, bottom: 0 }}>
          <XAxis
            dataKey="label"
            tick={{ fontSize: 10, fill: 'var(--color-ink-faint)' }}
            interval="preserveStartEnd"
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
          <Bar dataKey="count" fill="var(--color-signal)" radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartPanel>
  )
}

export default HistogramChart
