"""
Thin wrapper around the Prediction Engine (Phase 1). The fitted model,
X_test/y_test/y_pred, and any other internal objects never leave this
function - only the fields PredictionResponse actually needs go back to
the router.
"""

from src.prediction_engine import run_prediction_engine

from backend.schemas.responses import PredictionResponse
from backend.services.upload_service import get_upload_path
from backend.utils.validation import validate_target_is_trainable


def run_prediction(upload_id: str, target_column: str) -> PredictionResponse:
    file_path = str(get_upload_path(upload_id))
    validate_target_is_trainable(file_path, target_column)

    result = run_prediction_engine(file_path, target_column)

    return PredictionResponse(
        model_name=result["model_name"],
        accuracy=result["accuracy"],
        training_samples=result["training_samples"],
        testing_samples=result["testing_samples"],
        possible_id_columns=result["possible_id_columns"],
        converted_numeric_columns=result["converted_numeric_columns"],
        warnings=result["warnings"],
    )
