import Card from '@/components/Card'

/**
 * Will render chart_data from POST /analyze (histograms, category
 * counts, correlation heatmap, target distribution) using Recharts in
 * a later phase. No chart rendering yet - Phase 4A is layout only.
 */
function Charts() {
  return <Card eyebrow="Visualization" title="Charts" />
}

export default Charts
