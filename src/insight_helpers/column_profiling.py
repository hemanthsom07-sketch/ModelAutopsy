"""
Per-column profiling: what TYPE a column is, and summary statistics for
numeric and categorical columns.
"""

import pandas as pd

from src.insight_helpers.utils import clean_scalar, safe_float, safe_percentage


def is_binary_numeric_column(series):
    """
    True for a numeric column with exactly two distinct non-null values
    (e.g. a 0/1 flag like SeniorCitizen). Native boolean-dtype columns are
    reported as "boolean" instead - see infer_column_type below.
    """
    if pd.api.types.is_bool_dtype(series):
        return False
    if not pd.api.types.is_numeric_dtype(series):
        return False
    return series.dropna().nunique() == 2


def infer_column_type(series, column_name, converted_numeric_columns, possible_id_columns):
    """
    Decides a human-friendly "inferred type" for a column, checked in
    this priority order:

      1. possible identifier  - flagged by the ID-uniqueness heuristic
      2. datetime              - pandas parsed it as a real date/time
      3. boolean                - True/False values
      4. binary numeric         - numeric with exactly two distinct values
      5. converted numeric     - was text, but looked like numbers
      6. numeric                 - normal numeric dtype
      7. categorical             - everything else (text)

    This is a labelling convenience for the dashboard, not a strict
    guarantee - "possible identifier" in particular is still a heuristic.
    """
    if column_name in possible_id_columns:
        return "possible identifier"

    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"

    if pd.api.types.is_bool_dtype(series):
        return "boolean"

    if is_binary_numeric_column(series):
        return "binary numeric"

    if column_name in converted_numeric_columns:
        return "converted numeric"

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    return "categorical"


def build_column_metadata(data, converted_numeric_columns, possible_id_columns):
    """
    Builds a list of metadata dictionaries, one per column, in the
    dataset's original column order (a list, not a dict, so the frontend
    can render it as a table in the original column order).
    """
    total_rows = len(data)
    metadata = []

    for column_name in data.columns:
        series = data[column_name]
        missing_count = int(series.isnull().sum())
        unique_count = int(series.nunique(dropna=True))

        metadata.append({
            "column": column_name,
            "dtype": str(series.dtype),
            "inferred_type": infer_column_type(
                series, column_name, converted_numeric_columns, possible_id_columns
            ),
            "missing_count": missing_count,
            "missing_percentage": safe_percentage(missing_count, total_rows),
            "unique_count": unique_count,
            "unique_percentage": safe_percentage(unique_count, total_rows),
        })

    return metadata


def numeric_column_stats(series):
    """
    Summary statistics for a single numeric column. Outliers are flagged
    using the standard 1.5*IQR rule - a common, well-known convention,
    not the only valid definition of an outlier.
    """
    values = series.dropna()
    count = len(values)

    if count == 0:
        return {
            "count": 0, "mean": None, "median": None, "minimum": None,
            "maximum": None, "standard_deviation": None, "variance": None,
            "q1": None, "q3": None, "iqr": None,
            "outlier_count": 0, "outlier_percentage": None,
        }

    q1 = values.quantile(0.25)
    q3 = values.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = values[(values < lower_bound) | (values > upper_bound)]

    return {
        "count": count,
        "mean": safe_float(values.mean()),
        "median": safe_float(values.median()),
        "minimum": safe_float(values.min()),
        "maximum": safe_float(values.max()),
        # Sample standard deviation/variance need at least 2 points -
        # otherwise they are genuinely undefined, not zero.
        "standard_deviation": safe_float(values.std()) if count > 1 else None,
        "variance": safe_float(values.var()) if count > 1 else None,
        "q1": safe_float(q1),
        "q3": safe_float(q3),
        "iqr": safe_float(iqr),
        "outlier_count": int(len(outliers)),
        "outlier_percentage": safe_percentage(len(outliers), count),
    }


def categorical_column_stats(series, top_n=5, max_category_counts=20):
    """
    Summary statistics for a single categorical column. `category_counts`
    is capped at `max_category_counts` so a stray high-cardinality column
    doesn't blow up the response size.
    """
    values = series.dropna()
    count = len(values)

    if count == 0:
        return {
            "number_of_categories": 0,
            "most_common_value": None,
            "least_common_value": None,
            "top_categories": [],
            "category_counts": {},
        }

    value_counts = values.value_counts()

    top_categories = [
        {
            "value": str(value),
            "count": int(freq),
            "percentage": safe_percentage(freq, count),
        }
        for value, freq in value_counts.head(top_n).items()
    ]

    category_counts = {
        str(value): int(freq)
        for value, freq in value_counts.head(max_category_counts).items()
    }

    return {
        "number_of_categories": int(value_counts.shape[0]),
        "most_common_value": str(value_counts.index[0]),
        "least_common_value": str(value_counts.index[-1]),
        "top_categories": top_categories,
        "category_counts": category_counts,
    }


def binary_column_stats(series):
    """
    Summary for a binary numeric column (exactly two distinct values,
    e.g. 0/1): value counts, percentages, and missing values.

    IQR/outlier statistics and coefficient-of-variation-based checks
    (mean, std, variance, quartiles, "wide distribution") are NOT
    computed here - they assume a genuinely continuous spread, which a
    two-valued column does not have. See numeric_column_stats for that.
    """
    total = len(series)
    values = series.dropna()
    count = len(values)
    missing_count = total - count

    if count == 0:
        return {
            "count": 0,
            "missing_count": int(missing_count),
            "missing_percentage": safe_percentage(missing_count, total),
            "values": [],
        }

    value_counts = values.value_counts()

    value_breakdown = [
        {
            "value": clean_scalar(value),
            "count": int(freq),
            "percentage": safe_percentage(freq, count),
        }
        for value, freq in value_counts.items()
    ]

    return {
        "count": count,
        "missing_count": int(missing_count),
        "missing_percentage": safe_percentage(missing_count, total),
        "values": value_breakdown,
    }
