import { useState } from 'react'
import Card from '@/components/Card'
import StatItem from '@/components/StatItem'
import TargetColumnPicker from '@/components/TargetColumnPicker'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import { predictDataset, getErrorMessage, type PredictionResult } from '@/services/api'

interface PredictionResultsProps {
  uploadId: string | null
  columnNames: string[]
}

/**
 * Trains a classification model against the already-uploaded dataset via
 * POST /predict. Nothing runs automatically - the user picks a target
 * column and clicks "Run Prediction" explicitly.
 */
function PredictionResults({ uploadId, columnNames }: PredictionResultsProps) {
  const [targetColumn, setTargetColumn] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<PredictionResult | null>(null)

  if (!uploadId) {
    return <Card eyebrow="Model" title="Prediction Results" />
  }

  async function handleRunPrediction() {
    if (!targetColumn) return
    setIsLoading(true)
    setError(null)

    try {
      const prediction = await predictDataset(uploadId as string, targetColumn)
      setResult(prediction)
    } catch (err) {
      setError(getErrorMessage(err))
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  const status = isLoading ? 'Training…' : result ? 'Ready' : 'Awaiting run'

  return (
    <Card eyebrow="Model" title="Prediction Results" status={status}>
      <TargetColumnPicker
        columnNames={columnNames}
        selectedColumn={targetColumn}
        onSelectColumn={setTargetColumn}
        onSubmit={handleRunPrediction}
        isLoading={isLoading}
        buttonLabel="Run Prediction"
      />

      {isLoading && (
        <div className="mt-4">
          <LoadingSpinner label="Training model…" />
        </div>
      )}

      {error && !isLoading && (
        <div className="mt-4">
          <ErrorMessage message="Prediction failed" detail={error} />
        </div>
      )}

      {result && !isLoading && (
        <div className="mt-4 space-y-4">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <StatItem label="Model" value={result.model_name} />
            <StatItem label="Accuracy" value={`${(result.accuracy * 100).toFixed(2)}%`} />
            <StatItem label="Train samples" value={result.training_samples.toLocaleString()} />
            <StatItem label="Test samples" value={result.testing_samples.toLocaleString()} />
          </div>

          {result.possible_id_columns.length > 0 && (
            <p className="text-sm text-ink-soft">
              Excluded as possible identifiers:{' '}
              <span className="font-mono text-ink">{result.possible_id_columns.join(', ')}</span>
            </p>
          )}

          {result.converted_numeric_columns.length > 0 && (
            <p className="text-sm text-ink-soft">
              Converted to numeric:{' '}
              <span className="font-mono text-ink">
                {result.converted_numeric_columns.join(', ')}
              </span>
            </p>
          )}

          {result.warnings.length > 0 && (
            <ul className="space-y-2">
              {result.warnings.map((warning, index) => (
                <li
                  key={index}
                  className="rounded-lg border border-warning/40 bg-warning-soft px-3 py-2 text-sm text-ink-soft"
                >
                  {warning}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {!result && !isLoading && !error && (
        <p className="mt-4 text-sm text-ink-soft">
          Select a target column and run prediction to train a classification model.
        </p>
      )}
    </Card>
  )
}

export default PredictionResults
