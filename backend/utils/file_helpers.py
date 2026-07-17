"""
Small file-loading and JSON-safety helpers used across the backend.

load_dataset mirrors the load-by-extension logic that already exists
inside each src/ engine. It is duplicated here (rather than importing a
shared loader from src/) because the backend needs it for its OWN
pre-checks - validating an upload and inspecting a target column before
training - which happen before an engine is ever called. The engines
themselves are untouched and still load files their own way.

make_json_safe recursively converts numpy scalar types into plain Python
types. Most of the src/ engine output is already clean (Phase 1 and 2
convert explicitly in most places), but a few paths - notably sklearn's
classification_report - can still hand back numpy scalars, and raw numpy
types are not valid JSON.
"""

import numpy as np
import pandas as pd

from backend.config import ALLOWED_EXTENSIONS
from backend.utils.errors import ModelAutopsyError


def load_dataset(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    if file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    raise ModelAutopsyError(
        "unsupported_file",
        f"Unsupported file format. Only {', '.join(sorted(ALLOWED_EXTENSIONS))} are supported.",
    )


def make_json_safe(value):
    if isinstance(value, dict):
        return {key: make_json_safe(val) for key, val in value.items()}
    if isinstance(value, (list, tuple)):
        return [make_json_safe(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return None if np.isnan(value) else float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.ndarray):
        return make_json_safe(value.tolist())
    return value
