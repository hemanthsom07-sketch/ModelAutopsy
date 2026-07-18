import Card from '@/components/Card'

/**
 * Will render the POST /predict response (model name, accuracy,
 * train/test sizes, excluded ID columns, converted columns) in a
 * later phase.
 */
function PredictionResults() {
  return <Card eyebrow="Model" title="Prediction Results" />
}

export default PredictionResults
