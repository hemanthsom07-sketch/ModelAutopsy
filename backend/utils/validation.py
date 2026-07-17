"""
Shared validation used by both the Prediction and Autopsy services before
training anything. Reuses the Data Insight Engine's own target inspection
(src/insight_helpers/target_inspection.py, Phase 2) instead of
re-implementing target-suitability checks - this is the "required for
integration" touch point, and it only READS from src/, nothing in src/
was modified for it.
"""

from src.insight_helpers.target_inspection import inspect_target_column

from backend.utils.errors import ModelAutopsyError
from backend.utils.file_helpers import load_dataset


def validate_target_is_trainable(file_path, target_column):
    if not target_column:
        raise ModelAutopsyError(
            "missing_target_column", "target_column is required for this endpoint."
        )

    data = load_dataset(file_path)

    if target_column not in data.columns:
        raise ModelAutopsyError(
            "missing_target_column",
            f"Target column '{target_column}' was not found in the dataset.",
        )

    inspection = inspect_target_column(data, target_column)

    if inspection.get("error"):
        raise ModelAutopsyError("invalid_target_column", inspection["error"])

    if not inspection["classification_suitable"]:
        raise ModelAutopsyError("target_not_suitable", inspection["recommendation"])
