"""
Runs the Prediction Engine, then feeds its output straight into the
Model Autopsy Engine - the exact same two-step sequence main.py already
uses. Neither engine's logic is duplicated here, only orchestrated.
"""

from src.autopsy_engine import run_autopsy
from src.prediction_engine import run_prediction_engine

from backend.schemas.responses import AutopsyResponse
from backend.services.upload_service import get_upload_path
from backend.utils.file_helpers import make_json_safe
from backend.utils.validation import validate_target_is_trainable


def run_autopsy_pipeline(upload_id: str, target_column: str) -> AutopsyResponse:
    file_path = str(get_upload_path(upload_id))
    validate_target_is_trainable(file_path, target_column)

    prediction_result = run_prediction_engine(file_path, target_column)

    autopsy_result = run_autopsy(
        prediction_result["X_test"],
        prediction_result["y_test"],
        prediction_result["y_pred"],
        numeric_feature_names=prediction_result["numeric_feature_names"],
    )

    return AutopsyResponse(
        model_name=prediction_result["model_name"],
        accuracy=prediction_result["accuracy"],
        training_samples=prediction_result["training_samples"],
        testing_samples=prediction_result["testing_samples"],
        possible_id_columns=prediction_result["possible_id_columns"],
        converted_numeric_columns=prediction_result["converted_numeric_columns"],
        warnings=prediction_result["warnings"],
        autopsy=make_json_safe(autopsy_result),
    )
