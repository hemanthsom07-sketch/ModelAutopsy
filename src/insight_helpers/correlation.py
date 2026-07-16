"""
Correlation analysis for numeric columns. Reports association only -
never causation.
"""

import pandas as pd

from src.insight_helpers.utils import safe_float


def compute_correlation_analysis(data, numeric_columns, strong_threshold=0.80):
    if len(numeric_columns) < 2:
        return {
            "available": False,
            "reason": "At least 2 numeric columns are needed to compute correlations.",
            "threshold": strong_threshold,
            "matrix": {},
            "strong_positive_pairs": [],
            "strong_negative_pairs": [],
            "note": "Correlation describes association between columns, not causation.",
        }

    correlation_matrix = data[numeric_columns].corr()

    matrix_dict = {
        row_column: {
            col_column: safe_float(correlation_matrix.loc[row_column, col_column])
            for col_column in numeric_columns
        }
        for row_column in numeric_columns
    }

    strong_positive_pairs = []
    strong_negative_pairs = []

    for i, column_a in enumerate(numeric_columns):
        for column_b in numeric_columns[i + 1:]:
            value = correlation_matrix.loc[column_a, column_b]
            if pd.isna(value):
                continue
            if value >= strong_threshold:
                strong_positive_pairs.append({
                    "column_a": column_a,
                    "column_b": column_b,
                    "correlation": safe_float(value),
                })
            elif value <= -strong_threshold:
                strong_negative_pairs.append({
                    "column_a": column_a,
                    "column_b": column_b,
                    "correlation": safe_float(value),
                })

    strong_positive_pairs.sort(key=lambda item: item["correlation"], reverse=True)
    strong_negative_pairs.sort(key=lambda item: item["correlation"])

    return {
        "available": True,
        "reason": None,
        "threshold": strong_threshold,
        "matrix": matrix_dict,
        "strong_positive_pairs": strong_positive_pairs,
        "strong_negative_pairs": strong_negative_pairs,
        "note": "Correlation describes association between columns, not causation.",
    }
