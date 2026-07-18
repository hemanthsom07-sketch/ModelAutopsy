import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import ChartPanel from '@/components/charts/ChartPanel'
import type { CategoryCountData } from '@/services/api'

interface CategoryChartProps {
  column: string
  data: CategoryCountData
}

/** One horizontal bar chart per categorical column in chart_data.category_counts. */
function CategoryChart({ column, data }: CategoryChartProps) {
  const isEmpty = data.categories.length === 0
  const series = data.categories.map((category, index) => ({
    category,
    count: data.counts[index],
  }))

  return (
    <ChartPanel title={column} isEmpty={isEmpty} emptyMessage="No category values to plot">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={series} layout="vertical" margin={{ top: 4, right: 16, left: 8, bottom: 0 }}>
          <XAxis
            type="number"
            tick={{ fontSize: 10, fill: 'var(--color-ink-faint)' }}
            allowDecimals={false}
          />
          <YAxis
            type="category"
            dataKey="category"
            width={90}
            tick={{ fontSize: 10, fill: 'var(--color-ink-faint)' }}
          />
          <Tooltip
            contentStyle={{
              background: 'var(--color-surface)',
              border: '1px solid var(--color-border)',
              borderRadius: 8,
              fontSize: 12,
            }}
            labelStyle={{ color: 'var(--color-ink)' }}
          />
          <Bar dataKey="count" fill="var(--color-signal)" radius={[0, 3, 3, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartPanel>
  )
}

export default CategoryChart
