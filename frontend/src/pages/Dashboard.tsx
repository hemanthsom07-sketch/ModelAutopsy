import { useState } from 'react'
import UploadSection from '@/components/UploadSection'
import DatasetSummary from '@/components/DatasetSummary'
import DataQuality from '@/components/DataQuality'
import Charts from '@/components/Charts'
import Insights from '@/components/Insights'
import PredictionResults from '@/components/PredictionResults'
import AutopsyResults from '@/components/AutopsyResults'
import { uploadFile, analyzeDataset, getErrorMessage, type AnalyzeResponse } from '@/services/api'

/**
 * Main dashboard page. Owns the upload -> analyze workflow state and
 * passes the relevant slice down to each section. Charts, Prediction
 * Results, and Model Autopsy stay as Phase 4A placeholders - they are
 * out of scope for Phase 4B.
 */
function Dashboard() {
  const [analysis, setAnalysis] = useState<AnalyzeResponse | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleUpload(file: File) {
    setIsLoading(true)
    setError(null)

    try {
      const upload = await uploadFile(file)
      const result = await analyzeDataset(upload.upload_id)
      setAnalysis(result)
    } catch (err) {
      setError(getErrorMessage(err))
      setAnalysis(null)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <UploadSection onUpload={handleUpload} isLoading={isLoading} error={error} />

      <div className="mt-6">
        <DatasetSummary data={analysis?.dataset_summary ?? null} />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <DataQuality data={analysis?.data_quality ?? null} />
        <Insights data={analysis?.insights ?? null} />
      </div>

      <div className="mt-6">
        <Charts chartData={analysis?.chart_data ?? null} />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <PredictionResults />
        <AutopsyResults />
      </div>
    </main>
  )
}

export default Dashboard
