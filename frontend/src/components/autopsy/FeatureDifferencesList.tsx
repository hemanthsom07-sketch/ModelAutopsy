import type { CategoricalFeatureDifference, NumericFeatureDifference } from '@/services/api'

interface FeatureDifferencesListProps {
  numeric: NumericFeatureDifference[]
  categorical: CategoricalFeatureDifference[]
}

/**
 * Numeric and categorical differences use different metrics (standardized
 * mean difference vs. percentage points) and are kept in separate lists
 * rather than merged into one ranking - mixing them would imply the two
 * numbers are on the same scale, which they aren't (see autopsy_engine.py).
 */
function FeatureDifferencesList({ numeric, categorical }: FeatureDifferencesListProps) {
  if (numeric.length === 0 && categorical.length === 0) {
    return (
      <p className="text-sm text-ink-soft">
        No feature differences were calculated for this failure pattern.
      </p>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
      <div>
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-ink-soft">
          Numeric &middot; standardized mean difference
        </p>
        {numeric.length === 0 ? (
          <p className="text-sm text-ink-faint">None</p>
        ) : (
          <ul className="space-y-1.5">
            {numeric.map((item) => (
              <li
                key={item.feature}
                className="flex items-center justify-between rounded-lg border border-border bg-canvas/40 px-3 py-1.5 text-sm"
              >
                <span className="text-ink-soft">{item.feature}</span>
                <span className="font-mono text-ink" title={item.note}>
                  {item.value === null ? 'undefined' : item.value.toFixed(3)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <p className="mb-2 text-xs font-medium uppercase tracking-wide text-ink-soft">
          Categorical &middot; percentage-point difference
        </p>
        {categorical.length === 0 ? (
          <p className="text-sm text-ink-faint">None</p>
        ) : (
          <ul className="space-y-1.5">
            {categorical.map((item) => (
              <li
                key={item.feature}
                className="flex items-center justify-between rounded-lg border border-border bg-canvas/40 px-3 py-1.5 text-sm"
              >
                <span className="text-ink-soft">{item.feature}</span>
                <span className="font-mono text-ink">{item.value.toFixed(2)} pp</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default FeatureDifferencesList
