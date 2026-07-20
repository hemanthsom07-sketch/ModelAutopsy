import axios from 'axios'

const API_BASE_URL = 'https://modelautopsy.onrender.com'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ---------------------------------------------------------------------
// Types - mirror the backend's Pydantic schemas (backend/schemas/).
// Sections Phase 4B doesn't render yet (numeric_analysis, chart_data,
// etc.) are typed loosely since we don't reach into their internals
// yet; dataset_summary, data_quality, and insights - the three sections
// this phase actually renders - are fully typed.
// ---------------------------------------------------------------------

export interface UploadResponse {
  upload_id: string
  filename: string
  file_size_bytes: number
  rows: number
  columns: number
  column_names: string[]
}

export interface DatasetSummary {
  total_rows: number
  total_columns: number
  numeric_columns: number
  categorical_columns: number
  total_missing_values: number
  columns_with_missing_values: Record<string, number>
  duplicate_rows: number
  converted_numeric_columns: string[]
}

export interface DataQuality {
  duplicate_rows: number
  constant_columns: string[]
  near_constant_columns: string[]
  possible_id_columns: string[]
  numeric_looking_text_columns: string[]
  high_cardinality_columns: string[]
  low_variance_numeric_columns: string[]
  warnings: string[]
}

export interface HistogramData {
  bin_edges: number[]
  bin_counts: number[]
}

export interface CategoryCountData {
  categories: string[]
  counts: number[]
}

export interface MissingValuesChartData {
  columns: string[]
  missing_counts: number[]
}

export interface CorrelationHeatmapData {
  labels: string[]
  matrix: (number | null)[][]
}

export interface TargetDistributionChartData {
  classes: string[]
  counts: number[]
  percentages: number[]
}

export interface ChartData {
  histograms: Record<string, HistogramData>
  category_counts: Record<string, CategoryCountData>
  missing_values_chart: MissingValuesChartData
  correlation_heatmap: CorrelationHeatmapData | null
  target_distribution_chart: TargetDistributionChartData | null
}

export interface AnalyzeResponse {
  dataset_summary: DatasetSummary
  column_metadata: unknown[]
  numeric_analysis: Record<string, unknown>
  binary_analysis: Record<string, unknown>
  categorical_analysis: Record<string, unknown>
  data_quality: DataQuality
  correlation_analysis: Record<string, unknown>
  target_inspection: Record<string, unknown> | null
  chart_data: ChartData
  insights: string[]
}

export interface PredictionResult {
  model_name: string
  accuracy: number
  training_samples: number
  testing_samples: number
  possible_id_columns: string[]
  converted_numeric_columns: string[]
  warnings: string[]
}

export interface DominantFailure {
  actual_class: string
  predicted_class: string
  count: number
  percentage_of_errors: number
}

export interface NumericFeatureDifference {
  feature: string
  metric_type: string
  value: number | null
  failure_group_mean: number
  correct_group_mean: number
  note?: string
}

export interface CategoricalFeatureDifference {
  feature: string
  metric_type: string
  value: number
  failure_group_proportion: number
  correct_group_proportion: number
}

export interface ClassPerformanceMetrics {
  precision: number
  recall: number
  'f1-score': number
  support: number
}

/** class_performance mixes per-class metric objects with a bare "accuracy" number (from sklearn's classification_report). */
export type ClassPerformanceEntry = ClassPerformanceMetrics | number

export interface WeakClass {
  recall: number
  support: number
}

export interface AutopsyData {
  number_of_errors: number
  has_errors: boolean
  confusion_patterns: Record<string, number>
  dominant_failure: DominantFailure | null
  feature_differences: {
    numeric: NumericFeatureDifference[]
    categorical: CategoricalFeatureDifference[]
  }
  summary: string
  class_performance: Record<string, ClassPerformanceEntry>
  weak_classes: Record<string, WeakClass>
}

export interface AutopsyResult extends PredictionResult {
  autopsy: AutopsyData
}

interface ApiErrorBody {
  error: string
  detail: string
}

// ---------------------------------------------------------------------
// Implemented calls
// ---------------------------------------------------------------------

/**
 * POST /upload - sends the file as multipart/form-data.
 *
 * The Content-Type override below is required, not optional: the
 * apiClient instance defaults to 'application/json' (needed for
 * /analyze, /predict, /autopsy), and without this override that default
 * silently wins, the backend never sees a file field, and FastAPI
 * returns a 422 "field required" error instead of actually uploading
 * anything. Verified against the real backend both ways before settling
 * on this.
 */
export async function uploadFile(file: File): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post<UploadResponse>('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

/** POST /analyze - runs the Data Insight Engine only. */
export async function analyzeDataset(
  uploadId: string,
  targetColumn?: string,
): Promise<AnalyzeResponse> {
  const response = await apiClient.post<AnalyzeResponse>('/analyze', {
    upload_id: uploadId,
    target_column: targetColumn,
  })
  return response.data
}

/**
 * Extracts a friendly, displayable message from anything uploadFile or
 * analyzeDataset might throw - a clean backend error, a network failure,
 * or an unexpected JS error.
 */
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const body = error.response?.data as ApiErrorBody | undefined
    if (body?.detail) {
      return body.detail
    }
    if (error.code === 'ERR_NETWORK') {
      return 'Could not reach the server. Is the backend running?'
    }
    return error.message
  }
  if (error instanceof Error) {
    return error.message
  }
  return 'Something went wrong. Please try again.'
}

/** POST /predict - runs the Prediction Engine against an already-uploaded dataset. */
export async function predictDataset(
  uploadId: string,
  targetColumn: string,
): Promise<PredictionResult> {
  const response = await apiClient.post<PredictionResult>('/predict', {
    upload_id: uploadId,
    target_column: targetColumn,
  })
  return response.data
}

/** POST /autopsy - runs the Prediction Engine, then the Model Autopsy Engine. */
export async function autopsyDataset(
  uploadId: string,
  targetColumn: string,
): Promise<AutopsyResult> {
  const response = await apiClient.post<AutopsyResult>('/autopsy', {
    upload_id: uploadId,
    target_column: targetColumn,
  })
  return response.data
}
