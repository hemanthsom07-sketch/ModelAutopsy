import { useState, type ChangeEvent } from 'react'
import Card from '@/components/Card'
import LoadingSpinner from '@/components/LoadingSpinner'
import ErrorMessage from '@/components/ErrorMessage'

const ACCEPTED_EXTENSIONS = ['.csv', '.xlsx']

interface UploadSectionProps {
  onUpload: (file: File) => void
  isLoading: boolean
  error: string | null
}

function isAcceptedFile(file: File): boolean {
  const name = file.name.toLowerCase()
  return ACCEPTED_EXTENSIONS.some((extension) => name.endsWith(extension))
}

/**
 * File picker + upload trigger. Owns only its own local UI state (which
 * file is selected, client-side validation) - the actual upload/analyze
 * request and the resulting loading/error state live in Dashboard and
 * arrive here as props, so this component has no idea what happens
 * after it calls onUpload.
 */
function UploadSection({ onUpload, isLoading, error }: UploadSectionProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [validationError, setValidationError] = useState<string | null>(null)

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0]

    if (!file) {
      setSelectedFile(null)
      return
    }

    if (!isAcceptedFile(file)) {
      setValidationError('Please choose a .csv or .xlsx file.')
      setSelectedFile(null)
      event.target.value = ''
      return
    }

    setValidationError(null)
    setSelectedFile(file)
  }

  function handleUploadClick() {
    if (!selectedFile || isLoading) return
    onUpload(selectedFile)
  }

  const displayError = validationError ?? error
  const status = isLoading ? 'Analyzing…' : selectedFile ? 'Ready' : 'Awaiting dataset'

  return (
    <Card eyebrow="Input" title="Upload Dataset" status={status}>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-stretch">
        <label className="flex flex-1 cursor-pointer items-center justify-center rounded-lg border border-dashed border-border px-4 py-6 text-center text-sm text-ink-soft transition-colors hover:border-signal hover:text-ink">
          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={handleFileChange}
            disabled={isLoading}
            className="sr-only"
          />
          {selectedFile ? (
            <span className="font-mono text-ink">{selectedFile.name}</span>
          ) : (
            <span>Click to choose a .csv or .xlsx file</span>
          )}
        </label>

        <button
          type="button"
          onClick={handleUploadClick}
          disabled={!selectedFile || isLoading}
          className="rounded-lg bg-signal px-5 py-3 font-mono text-sm font-medium text-canvas transition-opacity disabled:cursor-not-allowed disabled:opacity-40"
        >
          Upload &amp; Analyze
        </button>
      </div>

      {isLoading && (
        <div className="mt-4">
          <LoadingSpinner label="Uploading and analyzing…" />
        </div>
      )}

      {displayError && !isLoading && (
        <div className="mt-4">
          <ErrorMessage message="Upload failed" detail={displayError} />
        </div>
      )}
    </Card>
  )
}

export default UploadSection
