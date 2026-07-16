"""
Optional inspection of a candidate target column - purely descriptive.
This module does NOT train anything; it only reports whether a column
looks more suitable for classification or regression, so the caller can
decide what to do next.
"""

import pandas as pd

from src.insight_helpers.utils import safe_percentage


CONTINUOUS_UNIQUE_COUNT_THRESHOLD = 20
CONTINUOUS_UNIQUE_RATIO_THRESHOLD = 0.05
IMBALANCE_MODERATE_THRESHOLD = 0.60
IMBALANCE_SEVERE_THRESHOLD = 0.80


def inspect_target_column(data, target_column):
    if target_column not in data.columns:
        return {
            "target_column": target_column,
            "error": f"'{target_column}' was not found in the dataset.",
        }

    series = data[target_column].dropna()
    total = len(series)

    if total == 0:
        return {
            "target_column": target_column,
            "error": f"'{target_column}' has no non-missing values to inspect.",
        }

    unique_count = series.nunique()
    unique_ratio = unique_count / total
    is_numeric = pd.api.types.is_numeric_dtype(series)

    # A numeric column with many distinct values relative to the dataset
    # looks continuous rather than categorical - classification isn't a
    # good fit for it as-is.
    looks_continuous = is_numeric and (
        unique_count > CONTINUOUS_UNIQUE_COUNT_THRESHOLD
        or unique_ratio > CONTINUOUS_UNIQUE_RATIO_THRESHOLD
    )

    if looks_continuous:
        return {
            "target_column": target_column,
            "detected_type": "numeric (likely continuous)",
            "unique_values": int(unique_count),
            "class_distribution": None,
            "imbalance_level": None,
            "classification_suitable": False,
            "recommendation": (
                "This target appears continuous and may require regression "
                "analysis. The current prediction engine primarily supports "
                "classification."
            ),
        }

    if unique_count < 2:
        return {
            "target_column": target_column,
            "detected_type": "numeric" if is_numeric else "categorical",
            "unique_values": int(unique_count),
            "class_distribution": None,
            "imbalance_level": None,
            "classification_suitable": False,
            "recommendation": (
                "This target has only one class in the data, so there is "
                "nothing for a classifier to distinguish between."
            ),
        }

    class_counts = series.value_counts()
    class_distribution = {
        str(class_value): {
            "count": int(count),
            "percentage": safe_percentage(count, total),
        }
        for class_value, count in class_counts.items()
    }

    majority_share = class_counts.iloc[0] / total

    if majority_share >= IMBALANCE_SEVERE_THRESHOLD:
        imbalance_level = "severe"
    elif majority_share >= IMBALANCE_MODERATE_THRESHOLD:
        imbalance_level = "moderate"
    else:
        imbalance_level = "balanced"

    return {
        "target_column": target_column,
        "detected_type": "numeric" if is_numeric else "categorical",
        "unique_values": int(unique_count),
        "class_distribution": class_distribution,
        "imbalance_level": imbalance_level,
        "classification_suitable": True,
        "recommendation": None,
    }
