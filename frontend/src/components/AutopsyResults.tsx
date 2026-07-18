import Card from '@/components/Card'

/**
 * Will render the `autopsy` block from POST /autopsy (dominant failure
 * pattern, confusion patterns, feature differences, weak classes,
 * summary) in a later phase.
 */
function AutopsyResults() {
  return <Card eyebrow="Failure Analysis" title="Model Autopsy" />
}

export default AutopsyResults
