"""
Response schemas.

Deeply-nested sections that come straight from the src/ engines
(dataset_summary, column_metadata, numeric_analysis, correlation_
analysis, chart_data, autopsy, etc.) are typed as Dict[str, Any] / List[
Dict[str, Any]] rather than fully re-modelled field-by-field. Those
shapes are already documented and enforced inside the engines themselves
(Phase 1 and 2); duplicating every nested field here as its own Pydantic
class would mean maintaining two parallel definitions of the same data
and would not add any real safety - it would only add a second place to
update every time an engine's output changes. Top-level scalars and
string lists ARE fully typed, since those are the fields callers will
actually branch on.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class RootResponse(BaseModel):
    project_name: str
    version: str
    status: str


class UploadResponse(BaseModel):
    upload_id: str
    filename: str
    file_size_bytes: int
    rows: int
    columns: int
    column_names: List[str]


class AnalyzeResponse(BaseModel):
    dataset_summary: Dict[str, Any]
    column_metadata: List[Dict[str, Any]]
    numeric_analysis: Dict[str, Any]
    binary_analysis: Dict[str, Any]
    categorical_analysis: Dict[str, Any]
    data_quality: Dict[str, Any]
    correlation_analysis: Dict[str, Any]
    target_inspection: Optional[Dict[str, Any]] = None
    chart_data: Dict[str, Any]
    insights: List[str]


class PredictionResponse(BaseModel):
    model_name: str
    accuracy: float
    training_samples: int
    testing_samples: int
    possible_id_columns: List[str]
    converted_numeric_columns: List[str]
    warnings: List[str]


class AutopsyResponse(PredictionResponse):
    """Everything PredictionResponse has, plus the autopsy results."""
    autopsy: Dict[str, Any]


class ErrorResponse(BaseModel):
    error: str
    detail: str
