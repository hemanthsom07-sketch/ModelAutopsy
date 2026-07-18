import Card from '@/components/Card'

/**
 * Will render data_quality from POST /analyze (missing values, possible
 * ID columns, constant/near-constant/high-cardinality flags, and the
 * generated warning sentences) in a later phase.
 */
function DataQuality() {
  return <Card eyebrow="Diagnostics" title="Data Quality" />
}

export default DataQuality
