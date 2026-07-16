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

import re

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


# Matches "id" bounded by an underscore/hyphen/space or the start/end of
# the name (case-insensitive) - e.g. "id", "customer_id", "order-id".
_ID_NAME_DELIMITED_PATTERN = re.compile(r"(^|[_\-\s])id([_\-\s]|$)")

# Matches a camelCase "Id" suffix (checked against the ORIGINAL casing, so
# plain lowercase words that merely end in "id" - rapid, void, solid -
# are not matched). "ID" (all caps) is checked separately below.
_ID_NAME_CAMEL_PATTERN = re.compile(r"[a-z]Id$")


def _name_suggests_identifier(column_name):
    """
    A deliberately narrow check for whether a column NAME looks like an
    identifier: "id", "customer_id", "CustomerId", "OrderID". Used only
    as supporting evidence for NUMERIC columns - see
    detect_possible_id_columns below for why text columns don't need it.
    """
    name = str(column_name)

    if _ID_NAME_DELIMITED_PATTERN.search(name.lower()):
        return True

    if _ID_NAME_CAMEL_PATTERN.search(name) or name.endswith("ID"):
        return True

    return False


def detect_possible_id_columns(df, columns, threshold=0.90):
    """
    Flags columns where almost every value is unique - a common sign of an
    identifier column (e.g. customerID) rather than a real predictive
    feature.

    TEXT columns: a high uniqueness ratio alone is treated as enough
    evidence. This is how the Prediction Engine has always used this
    function (it only ever passes text columns), so that behaviour is
    unchanged.

    NUMERIC columns: high uniqueness alone is also completely normal for
    an ordinary continuous measurement (a monetary total, a duration, a
    sensor reading) - not just for identifiers. So a numeric column is
    only flagged if its NAME also suggests an identifier. Without that
    extra evidence, a highly unique numeric column is treated as a
    continuous measurement, not an identifier.

    Either way, this remains a heuristic, not a guarantee - a genuinely
    predictive high-cardinality column could still trigger it, which is
    why callers should report this decision rather than silently act on it.

    Returns the list of column names that look ID-like.
    """
    id_columns = []
    total_rows = len(df)

    if total_rows == 0:
        return id_columns

    for column in columns:
        unique_ratio = df[column].nunique() / total_rows

        if unique_ratio <= threshold:
            continue

        if pd.api.types.is_numeric_dtype(df[column]):
            if _name_suggests_identifier(column):
                id_columns.append(column)
        else:
            id_columns.append(column)

    return id_columns
