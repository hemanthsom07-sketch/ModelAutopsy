import type { ReactNode } from 'react'
import Card from '@/components/Card'
import HistogramChart from '@/components/charts/HistogramChart'
import CategoryChart from '@/components/charts/CategoryChart'
import MissingValuesChart from '@/components/charts/MissingValuesChart'
import CorrelationHeatmap from '@/components/charts/CorrelationHeatmap'
import TargetDistributionChart from '@/components/charts/TargetDistributionChart'
import type { ChartData } from '@/services/api'

interface ChartsProps {
  chartData: ChartData | null
}

function ChartGrid({ children }: { children: ReactNode }) {
  return <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">{children}</div>
}

function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="mb-3 mt-6 text-xs font-medium uppercase tracking-wide text-ink-soft first:mt-0">
      {children}
    </p>
  )
}

/**
 * Renders every chart present in chart_data from POST /analyze. Nothing
 * is hidden behind a column selector - every histogram and every
 * category chart that exists in the response gets its own panel in a
 * responsive grid. Recharts only, no images.
 */
function Charts({ chartData }: ChartsProps) {
  if (!chartData) {
    return <Card eyebrow="Visualization" title="Charts" />
  }

  const histogramEntries = Object.entries(chartData.histograms)
  const categoryEntries = Object.entries(chartData.category_counts)

  return (
    <Card eyebrow="Visualization" title="Charts" status="Ready">
      {histogramEntries.length > 0 && (
        <>
          <SectionLabel>Numeric distributions</SectionLabel>
          <ChartGrid>
            {histogramEntries.map(([column, data]) => (
              <HistogramChart key={column} column={column} data={data} />
            ))}
          </ChartGrid>
        </>
      )}

      {categoryEntries.length > 0 && (
        <>
          <SectionLabel>Category breakdown</SectionLabel>
          <ChartGrid>
            {categoryEntries.map(([column, data]) => (
              <CategoryChart key={column} column={column} data={data} />
            ))}
          </ChartGrid>
        </>
      )}

      <SectionLabel>Dataset diagnostics</SectionLabel>
      <ChartGrid>
        <MissingValuesChart data={chartData.missing_values_chart} />
        <CorrelationHeatmap data={chartData.correlation_heatmap} />
        <TargetDistributionChart data={chartData.target_distribution_chart} />
      </ChartGrid>
    </Card>
  )
}

export default Charts
