import { Cell, Legend, Pie, PieChart, ResponsiveContainer, Tooltip } from 'recharts'
import ChartPanel from '@/components/charts/ChartPanel'
import type { TargetDistributionChartData } from '@/services/api'

interface TargetDistributionChartProps {
  data: TargetDistributionChartData | null
}

const SLICE_COLORS = [
  'var(--color-signal)',
  'var(--color-warning)',
  'var(--color-critical)',
  'var(--color-ink-soft)',
]

/**
 * Target class distribution as a donut chart. No target column is
 * selected yet in the current workflow (POST /analyze is called without
 * one), so this reliably shows its empty state today - it will populate
 * once target selection is added in a later phase.
 */
function TargetDistributionChart({ data }: TargetDistributionChartProps) {
  const isEmpty = !data || data.classes.length === 0
  const series = data
    ? data.classes.map((className, index) => ({ name: className, value: data.counts[index] }))
    : []

  return (
    <ChartPanel
      title="Target class distribution"
      isEmpty={isEmpty}
      emptyMessage="Select a target column to see its class distribution"
    >
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={series}
            dataKey="value"
            nameKey="name"
            innerRadius="45%"
            outerRadius="75%"
            paddingAngle={2}
          >
            {series.map((entry, index) => (
              <Cell key={entry.name} fill={SLICE_COLORS[index % SLICE_COLORS.length]} />
            ))}
          </Pie>
          <Legend wrapperStyle={{ fontSize: 11, color: 'var(--color-ink-soft)' }} />
          <Tooltip
            contentStyle={{
              background: 'var(--color-surface)',
              border: '1px solid var(--color-border)',
              borderRadius: 8,
              fontSize: 12,
            }}
            labelStyle={{ color: 'var(--color-ink)' }}
          />
        </PieChart>
      </ResponsiveContainer>
    </ChartPanel>
  )
}

export default TargetDistributionChart
