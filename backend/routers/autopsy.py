from fastapi import APIRouter

from backend.schemas.requests import UploadRequest
from backend.schemas.responses import AutopsyResponse
from backend.services.autopsy_service import run_autopsy_pipeline

router = APIRouter()


@router.post("/autopsy", response_model=AutopsyResponse, tags=["autopsy"])
def autopsy_dataset(request: UploadRequest):
    """Runs the Prediction Engine, then the Model Autopsy Engine. target_column is required."""
    return run_autopsy_pipeline(request.upload_id, request.target_column)
