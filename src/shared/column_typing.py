"""
Shared column-typing helpers used by both the Data Insight Engine and the
Prediction Engine.

These are schema-level decisions (what TYPE is this column, does it look
like an identifier) rather than statistics fitted for modelling, so it is
safe to compute them on the full dataset before any train/test split.
Neither function looks at the target column or produces a value that
becomes part of a trained model's input, so there is no data-leakage risk
in using the full dataset for these two checks. This is different from
things like imputation medians or one-hot vocabulary, which DO need to be
fit on the training split only (see prediction_engine.py).
"""

import pandas as pd


def convert_numeric_looking_columns(df, columns, threshold=0.90):
    """
    Some columns are stored as text but are really numbers (e.g. the Telco
    TotalCharges column). For each column in `columns`, this tries to
    convert it to a numeric column. If more than `threshold` of the values
    convert successfully, the column is replaced in-place with its numeric
    version.

    Returns the list of column names that were converted.
    """
    converted_columns = []

    for column in columns:
        converted = pd.to_numeric(df[column], errors="coerce")
        conversion_ratio = converted.notna().mean()

        if conversion_ratio > threshold:
            df[column] = converted
            converted_columns.append(column)

    return converted_columns


def detect_possible_id_columns(df, columns, threshold=0.90):
    """
    Flags columns where almost every value is unique - a common sign of an
    identifier column (e.g. customerID) rather than a real predictive
    feature.

    This is a heuristic based on a uniqueness ratio, not a guarantee. A
    genuinely predictive high-cardinality column could also trigger it,
    which is why callers should report this decision rather than silently
    act on it.

    Returns the list of column names that look ID-like.
    """
    id_columns = []
    total_rows = len(df)

    if total_rows == 0:
        return id_columns

    for column in columns:
        unique_ratio = df[column].nunique() / total_rows

        if unique_ratio > threshold:
            id_columns.append(column)

    return id_columns
