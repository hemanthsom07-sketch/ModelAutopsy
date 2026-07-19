interface TargetColumnPickerProps {
  columnNames: string[]
  selectedColumn: string
  onSelectColumn: (column: string) => void
  onSubmit: () => void
  isLoading: boolean
  buttonLabel: string
}

/**
 * Column dropdown + trigger button shared by PredictionResults and
 * AutopsyResults - both need the same "pick a target, then run"
 * interaction, just against a different endpoint.
 */
function TargetColumnPicker({
  columnNames,
  selectedColumn,
  onSelectColumn,
  onSubmit,
  isLoading,
  buttonLabel,
}: TargetColumnPickerProps) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-end">
      <label className="flex-1">
        <span className="mb-1 block font-mono text-[11px] uppercase tracking-widest text-ink-faint">
          Target column
        </span>
        <select
          value={selectedColumn}
          onChange={(event) => onSelectColumn(event.target.value)}
          disabled={isLoading || columnNames.length === 0}
          className="w-full rounded-lg border border-border bg-canvas px-3 py-2 text-sm text-ink disabled:cursor-not-allowed disabled:opacity-60"
        >
          <option value="" disabled>
            Select a column…
          </option>
          {columnNames.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </label>

      <button
        type="button"
        onClick={onSubmit}
        disabled={!selectedColumn || isLoading}
        className="rounded-lg bg-signal px-5 py-2.5 font-mono text-sm font-medium text-canvas transition-opacity disabled:cursor-not-allowed disabled:opacity-40"
      >
        {buttonLabel}
      </button>
    </div>
  )
}

export default TargetColumnPicker
