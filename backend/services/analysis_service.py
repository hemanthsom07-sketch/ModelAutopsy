"""
Thin wrapper around the Data Insight Engine (Phase 2). This file computes
nothing itself - it resolves the upload_id to a file path, calls
generate_data_insights exactly as main.py does, and shapes the result
into AnalyzeResponse.
"""

from src.data_insight_engine import generate_data_insights

from backend.schemas.responses import AnalyzeResponse
from backend.services.upload_service import get_upload_path
from backend.utils.file_helpers import make_json_safe


def run_analysis(upload_id: str, target_column: str = None) -> AnalyzeResponse:
    file_path = str(get_upload_path(upload_id))

    result = generate_data_insights(file_path, target_column=target_column)

    return AnalyzeResponse(
        dataset_summary=make_json_safe(result["dataset_summary"]),
        column_metadata=make_json_safe(result["column_metadata"]),
        numeric_analysis=make_json_safe(result["numeric_analysis"]),
        binary_analysis=make_json_safe(result["binary_analysis"]),
        categorical_analysis=make_json_safe(result["categorical_analysis"]),
        data_quality=make_json_safe(result["data_quality"]),
        correlation_analysis=make_json_safe(result["correlation_analysis"]),
        target_inspection=make_json_safe(result["target_inspection"]),
        chart_data=make_json_safe(result["chart_data"]),
        insights=result["insights"],
    )
