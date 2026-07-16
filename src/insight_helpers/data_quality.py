"""
Dataset-level data quality checks: duplicates, constant/near-constant
columns, high-cardinality columns, low-variance numeric columns, and
possible identifier columns (reusing the same heuristic the Prediction
Engine uses, from src/shared/column_typing.py).
"""

from src.shared.column_typing import detect_possible_id_columns
from src.insight_helpers.utils import safe_percentage


NEAR_CONSTANT_THRESHOLD = 0.95     # one value makes up >95% of non-null rows
HIGH_CARDINALITY_RATIO = 0.50      # more than half the rows are unique values
LOW_VARIANCE_CV_THRESHOLD = 0.05   # std is less than 5% of the mean


def find_constant_and_near_constant_columns(data):
    """
    Constant: only one distinct non-null value appears at all.
    Near-constant: more than one value appears, but a single value
    dominates (over NEAR_CONSTANT_THRESHOLD of non-null rows).
    Both are heuristics for "this column carries little to no
    information" - a column that is entirely missing is skipped here
    (it gets its own missing-values warning instead).
    """
    constant_columns = []
    near_constant_columns = []

    for column in data.columns:
        values = data[column].dropna()
        if len(values) == 0:
            continue

        value_counts = values.value_counts()
        top_share = value_counts.iloc[0] / len(values)

        if value_counts.shape[0] == 1:
            constant_columns.append(column)
        elif top_share > NEAR_CONSTANT_THRESHOLD:
            near_constant_columns.append(column)

    return constant_columns, near_constant_columns


def find_high_cardinality_columns(data, categorical_columns):
    """
    Categorical columns where more than HIGH_CARDINALITY_RATIO of rows
    are unique values - a broader, softer signal than the ID-detection
    heuristic used for modelling (a column can be both).
    """
    total_rows = len(data)
    high_cardinality_columns = []

    if total_rows == 0:
        return high_cardinality_columns

    for column in categorical_columns:
        unique_ratio = data[column].nunique() / total_rows
        if unique_ratio > HIGH_CARDINALITY_RATIO:
            high_cardinality_columns.append(column)

    return high_cardinality_columns


def find_low_variance_numeric_columns(data, numeric_columns):
    """
    Numeric columns whose spread is tiny relative to their own mean
    (coefficient of variation). Flags columns that are unlikely to be
    useful predictors, without claiming they are useless.
    """
    low_variance_columns = []

    for column in numeric_columns:
        values = data[column].dropna()
        if len(values) < 2:
            continue

        mean = values.mean()
        std = values.std()

        if abs(mean) > 1e-8:
            coefficient_of_variation = abs(std / mean)
            if coefficient_of_variation < LOW_VARIANCE_CV_THRESHOLD:
                low_variance_columns.append(column)
        elif std < 1e-8:
            low_variance_columns.append(column)

    return low_variance_columns


def run_data_quality_checks(
    data,
    numeric_columns,
    categorical_columns,
    converted_numeric_columns,
    id_uniqueness_threshold=0.90,
):
    total_rows = len(data)

    missing_values = data.isnull().sum()
    columns_with_missing = missing_values[missing_values > 0]

    duplicate_rows = int(data.duplicated().sum())

    constant_columns, near_constant_columns = find_constant_and_near_constant_columns(data)

    # Possible IDs are checked across ALL columns here (not just text
    # columns), because a plain numeric "id" column is just as much an
    # identifier as a text one. This is intentionally broader than the
    # Prediction Engine's own check, which only looks at text columns
    # before modelling - that logic is left untouched this phase.
    possible_id_columns = detect_possible_id_columns(
        data, list(data.columns), threshold=id_uniqueness_threshold
    )

    high_cardinality_columns = find_high_cardinality_columns(data, categorical_columns)
    low_variance_columns = find_low_variance_numeric_columns(data, numeric_columns)

    warnings = []

    if total_rows == 0:
        warnings.append("The dataset has no rows.")

    for column, count in columns_with_missing.items():
        percentage = safe_percentage(count, total_rows)
        suffix = f" ({percentage}% of rows)." if percentage is not None else "."
        warnings.append(f"{column} contains {int(count)} missing values{suffix}")

    if duplicate_rows > 0:
        warnings.append(f"The dataset contains {duplicate_rows} duplicate rows.")

    for column in possible_id_columns:
        warnings.append(
            f"{column} appears to be an identifier because nearly every value is unique."
        )

    for column in converted_numeric_columns:
        warnings.append(
            f"{column} was stored as text but most values are numeric, "
            f"so it was interpreted as a numeric column."
        )

    for column in constant_columns:
        warnings.append(f"{column} has the same value in every row and adds no information.")

    for column in near_constant_columns:
        warnings.append(f"{column} is dominated by a single value in almost every row.")

    for column in high_cardinality_columns:
        warnings.append(
            f"{column} has a large number of distinct values relative to the dataset size."
        )

    for column in low_variance_columns:
        warnings.append(f"{column} shows very little spread around its average value.")

    return {
        "duplicate_rows": duplicate_rows,
        "constant_columns": constant_columns,
        "near_constant_columns": near_constant_columns,
        "possible_id_columns": possible_id_columns,
        "numeric_looking_text_columns": converted_numeric_columns,
        "high_cardinality_columns": high_cardinality_columns,
        "low_variance_numeric_columns": low_variance_columns,
        "warnings": warnings,
    }
