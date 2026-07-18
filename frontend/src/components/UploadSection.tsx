import Card from '@/components/Card'

/**
 * Entry point of the dashboard. Will hold drag-and-drop upload,
 * file validation, and the resulting upload_id in a later phase
 * (see backend POST /upload).
 */
function UploadSection() {
  return <Card eyebrow="Input" title="Upload Dataset" />
}

export default UploadSection
