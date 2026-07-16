import pandas as pd

from src.shared.column_typing import convert_numeric_looking_columns
from src.insight_helpers.column_profiling import (
    build_column_metadata,
    numeric_column_stats,
    categorical_column_stats,
    is_binary_numeric_column,
    binary_column_stats,
)
from src.insight_helpers.data_quality import run_data_quality_checks
from src.insight_helpers.correlation import compute_correlation_analysis
from src.insight_helpers.target_inspection import inspect_target_column
from src.insight_helpers.chart_data import build_chart_data
from src.insight_helpers.insight_text import generate_insights


def generate_data_insights(
    file_path,
    target_column=None,
    numeric_conversion_threshold=0.90,
    id_uniqueness_threshold=0.90,
    correlation_threshold=0.80,
):
    """
    Runs a full, automatic analysis of a tabular dataset - no machine
    learning happens here. This is the "understand the dataset" stage
    that runs before (and independently of) any model training.

    target_column is optional. If given, the target column is inspected
    (class balance, classification vs regression suitability) but never
    used to train anything in this function.
    """

    # ---- Load dataset based on file type ----
    if file_path.endswith(".csv"):
        data = pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        data = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format")

    total_rows = data.shape[0]
    total_columns = data.shape[1]

    # ---- Column typing (shared with the Prediction Engine, so both
    #      engines agree on what counts as numeric vs text) ----
    text_columns = data.select_dtypes(include=["object", "string"]).columns.tolist()
    converted_numeric_columns = convert_numeric_looking_columns(
        data, text_columns, threshold=numeric_conversion_threshold
    )

    numeric_columns = data.select_dtypes(include="number").columns.tolist()
    categorical_columns = data.select_dtypes(include=["object", "string"]).columns.tolist()

    # ---- Data quality (also finds possible ID columns, across ALL
    #      columns - broader than the Prediction Engine's text-only check) ----
    data_quality = run_data_quality_checks(
        data,
        numeric_columns,
        categorical_columns,
        converted_numeric_columns,
        id_uniqueness_threshold=id_uniqueness_threshold,
    )

    # ---- Per-column metadata and statistics ----
    column_metadata = build_column_metadata(
        data, converted_numeric_columns, data_quality["possible_id_columns"]
    )

    # Binary numeric columns (exactly two distinct values, e.g. a 0/1
    # flag) get their own stats instead of IQR/outlier and coefficient-
    # of-variation statistics, which assume a genuinely continuous spread.
    binary_numeric_columns = [
        column for column in numeric_columns if is_binary_numeric_column(data[column])
    ]
    regular_numeric_columns = [
        column for column in numeric_columns if column not in binary_numeric_columns
    ]

    numeric_analysis = {
        column: numeric_column_stats(data[column]) for column in regular_numeric_columns
    }

    binary_analysis = {
        column: binary_column_stats(data[column]) for column in binary_numeric_columns
    }

    categorical_analysis = {
        column: categorical_column_stats(data[column]) for column in categorical_columns
    }

    # ---- Correlation (numeric columns only) ----
    correlation_analysis = compute_correlation_analysis(
        data, numeric_columns, strong_threshold=correlation_threshold
    )

    # ---- Optional target column inspection - descriptive only, no training ----
    target_inspection_result = None
    if target_column is not None:
        target_inspection_result = inspect_target_column(data, target_column)

    # ---- Chart-ready JSON for the future frontend (no images) ----
    chart_data = build_chart_data(
        data, numeric_columns, categorical_columns,
        correlation_analysis, target_inspection_result,
    )

    # ---- Dataset-level summary (kept for quick overview cards) ----
    missing_values = data.isnull().sum()
    total_missing_values = int(missing_values.sum())
    columns_with_missing_values = (
        missing_values[missing_values > 0].sort_values(ascending=False).to_dict()
    )

    dataset_summary = {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "numeric_columns": len(numeric_columns),
        "categorical_columns": len(categorical_columns),
        "total_missing_values": total_missing_values,
        "columns_with_missing_values": columns_with_missing_values,
        "duplicate_rows": data_quality["duplicate_rows"],
        "converted_numeric_columns": converted_numeric_columns,
    }

    # ---- Deterministic, human-readable insights (built last - draws on
    #      every section computed above) ----
    insights = generate_insights(
        dataset_summary, data_quality, correlation_analysis,
        numeric_analysis, binary_analysis, target_inspection_result,
    )

    return {
        "data": data,
        "dataset_summary": dataset_summary,
        "column_metadata": column_metadata,
        "numeric_analysis": numeric_analysis,
        "binary_analysis": binary_analysis,
        "categorical_analysis": categorical_analysis,
        "data_quality": data_quality,
        "correlation_analysis": correlation_analysis,
        "target_inspection": target_inspection_result,
        "chart_data": chart_data,
        "insights": insights,
    }
