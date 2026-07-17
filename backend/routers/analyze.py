from fastapi import APIRouter

from backend.schemas.requests import UploadRequest
from backend.schemas.responses import AnalyzeResponse
from backend.services.analysis_service import run_analysis

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse, tags=["analyze"])
def analyze_dataset(request: UploadRequest):
    """Runs the Data Insight Engine only - no model is trained here."""
    return run_analysis(request.upload_id, request.target_column)
