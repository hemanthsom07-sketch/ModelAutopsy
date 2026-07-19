import { useState, type ReactNode } from 'react'
import Card from '@/components/Card'
import StatItem from '@/components/StatItem'
import TargetColumnPicker from '@/components/TargetColumnPicker'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'
import DominantFailureCard from '@/components/autopsy/DominantFailureCard'
import ConfusionPatternsList from '@/components/autopsy/ConfusionPatternsList'
import ClassPerformanceTable from '@/components/autopsy/ClassPerformanceTable'
import WeakClassesList from '@/components/autopsy/WeakClassesList'
import FeatureDifferencesList from '@/components/autopsy/FeatureDifferencesList'
import { autopsyDataset, getErrorMessage, type AutopsyResult } from '@/services/api'

interface AutopsyResultsProps {
  uploadId: string | null
  columnNames: string[]
}

function SubSectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="mb-2 mt-5 text-xs font-medium uppercase tracking-wide text-ink-soft first:mt-0">
      {children}
    </p>
  )
}

/**
 * Runs the Prediction Engine then the Model Autopsy Engine via
 * POST /autopsy. Nothing runs automatically - the user picks a target
 * column and clicks "Run Autopsy" explicitly. Every section the backend
 * returns is rendered: overview stats, the auto-generated summary,
 * dominant failure, confusion patterns, feature differences, class
 * performance, and weak classes.
 */
function AutopsyResults({ uploadId, columnNames }: AutopsyResultsProps) {
  const [targetColumn, setTargetColumn] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AutopsyResult | null>(null)

  if (!uploadId) {
    return <Card eyebrow="Failure Analysis" title="Model Autopsy" />
  }

  async function handleRunAutopsy() {
    if (!targetColumn) return
    setIsLoading(true)
    setError(null)

    try {
      const autopsy = await autopsyDataset(uploadId as string, targetColumn)
      setResult(autopsy)
    } catch (err) {
      setError(getErrorMessage(err))
      setResult(null)
    } finally {
      setIsLoading(false)
    }
  }

  const status = isLoading ? 'Analyzing failures…' : result ? 'Ready' : 'Awaiting run'

  return (
    <Card eyebrow="Failure Analysis" title="Model Autopsy" status={status}>
      <TargetColumnPicker
        columnNames={columnNames}
        selectedColumn={targetColumn}
        onSelectColumn={setTargetColumn}
        onSubmit={handleRunAutopsy}
        isLoading={isLoading}
        buttonLabel="Run Autopsy"
      />

      {isLoading && (
        <div className="mt-4">
          <LoadingSpinner label="Training model and analyzing failures…" />
        </div>
      )}

      {error && !isLoading && (
        <div className="mt-4">
          <ErrorMessage message="Autopsy failed" detail={error} />
        </div>
      )}

      {result && !isLoading && (
        <div className="mt-4">
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            <StatItem label="Model" value={result.model_name} />
            <StatItem label="Accuracy" value={`${(result.accuracy * 100).toFixed(2)}%`} />
            <StatItem label="Errors" value={result.autopsy.number_of_errors.toLocaleString()} />
            <StatItem label="Test samples" value={result.testing_samples.toLocaleString()} />
          </div>

          <p className="mt-4 rounded-lg border border-border bg-canvas/40 px-4 py-3 text-sm leading-relaxed text-ink-soft">
            {result.autopsy.summary}
          </p>

          {result.autopsy.has_errors && result.autopsy.dominant_failure && (
            <>
              <SubSectionLabel>Dominant failure</SubSectionLabel>
              <DominantFailureCard data={result.autopsy.dominant_failure} />
            </>
          )}

          {result.autopsy.has_errors && (
            <>
              <SubSectionLabel>Confusion patterns</SubSectionLabel>
              <ConfusionPatternsList data={result.autopsy.confusion_patterns} />

              <SubSectionLabel>Feature differences</SubSectionLabel>
              <FeatureDifferencesList
                numeric={result.autopsy.feature_differences.numeric}
                categorical={result.autopsy.feature_differences.categorical}
              />
            </>
          )}

          <SubSectionLabel>Class performance</SubSectionLabel>
          <ClassPerformanceTable data={result.autopsy.class_performance} />

          <SubSectionLabel>Weak classes</SubSectionLabel>
          <WeakClassesList data={result.autopsy.weak_classes} />

          {result.possible_id_columns.length > 0 && (
            <p className="mt-4 text-sm text-ink-soft">
              Excluded as possible identifiers:{' '}
              <span className="font-mono text-ink">{result.possible_id_columns.join(', ')}</span>
            </p>
          )}

          {result.warnings.length > 0 && (
            <ul className="mt-3 space-y-2">
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
          Select a target column and run the autopsy to see model failure analysis.
        </p>
      )}
    </Card>
  )
}

export default AutopsyResults
