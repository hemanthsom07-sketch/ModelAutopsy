"""
Small shared helpers for the Phase 2 Data Insight Engine modules.

These mostly exist so every number in the final output is safe to send
over an API later (no NaN, no numpy scalar types, no division-by-zero
crashes) without repeating the same checks in every module.
"""

import math


def safe_float(value):
    """
    Converts a value to a plain Python float, or None if it is NaN/None/
    infinite. Needed because raw NaN is not valid JSON.
    """
    if value is None:
        return None
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(value) or math.isinf(value):
        return None
    return value


def safe_percentage(part, whole, decimals=2):
    """Returns part/whole as a percentage, or None if whole is 0."""
    if not whole:
        return None
    return round((part / whole) * 100, decimals)


def clean_scalar(value):
    """
    Converts a numpy/pandas scalar into a plain Python int or float,
    preferring int when the value is a whole number - so a binary 0/1
    column reports its values as 0 and 1, not 0.0 and 1.0.
    """
    try:
        as_float = float(value)
    except (TypeError, ValueError):
        return value
    if as_float.is_integer():
        return int(as_float)
    return as_float
