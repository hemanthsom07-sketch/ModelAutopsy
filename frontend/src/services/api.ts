import axios from 'axios'

/**
 * Placeholder API layer for Phase 4A - infrastructure only.
 *
 * The axios instance below is configured and ready, but none of the
 * functions actually call the backend yet (see backend/routers/ for
 * the real endpoints: GET /, POST /upload, POST /analyze, POST /predict,
 * POST /autopsy). Wiring these up, defining response types, and handling
 * loading/error state is Phase 4B work.
 */

const API_BASE_URL = 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export async function uploadDataset(_file: File): Promise<never> {
  // TODO (Phase 4B): POST /upload as multipart/form-data
  throw new Error('uploadDataset is not implemented yet')
}

export async function analyzeDataset(
  _uploadId: string,
  _targetColumn?: string,
): Promise<never> {
  // TODO (Phase 4B): POST /analyze
  throw new Error('analyzeDataset is not implemented yet')
}

export async function predictDataset(
  _uploadId: string,
  _targetColumn: string,
): Promise<never> {
  // TODO (Phase 4B): POST /predict
  throw new Error('predictDataset is not implemented yet')
}

export async function autopsyDataset(
  _uploadId: string,
  _targetColumn: string,
): Promise<never> {
  // TODO (Phase 4B): POST /autopsy
  throw new Error('autopsyDataset is not implemented yet')
}
