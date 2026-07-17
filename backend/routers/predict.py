from fastapi import APIRouter

from backend.schemas.requests import UploadRequest
from backend.schemas.responses import PredictionResponse
from backend.services.prediction_service import run_prediction

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse, tags=["predict"])
def predict_dataset(request: UploadRequest):
    """Runs the Prediction Engine. target_column is required."""
    return run_prediction(request.upload_id, request.target_column)
