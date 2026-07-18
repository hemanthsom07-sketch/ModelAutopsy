import Card from '@/components/Card'

/**
 * Will render the dataset_summary block from POST /analyze (row/column
 * counts, missing values, duplicates, converted columns) as a row of
 * stat readouts in a later phase.
 */
function DatasetSummary() {
  return <Card eyebrow="Overview" title="Dataset Summary" />
}

export default DatasetSummary
