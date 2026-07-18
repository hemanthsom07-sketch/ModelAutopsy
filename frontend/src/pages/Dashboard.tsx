import UploadSection from '@/components/UploadSection'
import DatasetSummary from '@/components/DatasetSummary'
import DataQuality from '@/components/DataQuality'
import Charts from '@/components/Charts'
import Insights from '@/components/Insights'
import PredictionResults from '@/components/PredictionResults'
import AutopsyResults from '@/components/AutopsyResults'

/**
 * Main dashboard page. Sections are ordered the way a user actually
 * moves through the product: upload, understand the dataset, visualize
 * it, read the findings, train a model, see how it failed. Phase 4A
 * only lays out the shell - each section renders its own placeholder
 * card for now.
 */
function Dashboard() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <UploadSection />

      <div className="mt-6">
        <DatasetSummary />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <DataQuality />
        <Insights />
      </div>

      <div className="mt-6">
        <Charts />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        <PredictionResults />
        <AutopsyResults />
      </div>
    </main>
  )
}

export default Dashboard
