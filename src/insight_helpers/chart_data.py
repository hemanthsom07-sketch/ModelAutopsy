"""
Builds chart-ready JSON structures for the future frontend. No images,
no matplotlib, no PNGs - just plain numbers a JS charting library can
plot directly.
"""

import math
import numpy as np

from src.insight_helpers.utils import safe_float


DEFAULT_TOP_CATEGORIES_FOR_CHART = 15


def histogram_data(series, bins=None):
    values = series.dropna()
    count = len(values)

    if count == 0:
        return {"bin_edges": [], "bin_counts": []}

    if bins is None:
        # Bin count grows with sqrt(sample size) - a common simple rule
        # of thumb - kept within a readable range for very small or very
        # large columns.
        bins = int(min(30, max(5, round(math.sqrt(count)))))

    if values.min() == values.max():
        # A single repeated value can't be split into a real range.
        return {
            "bin_edges": [safe_float(values.min()), safe_float(values.min())],
            "bin_counts": [count],
        }

    bin_counts, bin_edges = np.histogram(values, bins=bins)

    return {
        "bin_edges": [safe_float(edge) for edge in bin_edges],
        "bin_counts": [int(c) for c in bin_counts],
    }


def category_count_chart(series, top_n=DEFAULT_TOP_CATEGORIES_FOR_CHART):
    values = series.dropna()
    if len(values) == 0:
        return {"categories": [], "counts": []}

    value_counts = values.value_counts()
    top = value_counts.head(top_n)

    categories = [str(v) for v in top.index]
    counts = [int(c) for c in top.values]

    remaining = value_counts.iloc[top_n:].sum()
    if remaining > 0:
        categories.append("Other")
        counts.append(int(remaining))

    return {"categories": categories, "counts": counts}


def missing_values_chart(data):
    missing = data.isnull().sum()
    return {
        "columns": missing.index.tolist(),
        "missing_counts": [int(v) for v in missing.values],
    }


def target_distribution_chart(class_distribution):
    if not class_distribution:
        return None
    classes = list(class_distribution.keys())
    counts = [class_distribution[c]["count"] for c in classes]
    percentages = [class_distribution[c]["percentage"] for c in classes]
    return {"classes": classes, "counts": counts, "percentages": percentages}


def build_chart_data(
    data,
    numeric_columns,
    categorical_columns,
    correlation_analysis,
    target_inspection_result,
):
    histograms = {
        column: histogram_data(data[column]) for column in numeric_columns
    }

    category_counts = {
        column: category_count_chart(data[column]) for column in categorical_columns
    }

    correlation_heatmap = None
    if correlation_analysis and correlation_analysis.get("available"):
        labels = list(correlation_analysis["matrix"].keys())
        correlation_heatmap = {
            "labels": labels,
            "matrix": [
                [correlation_analysis["matrix"][row][col] for col in labels]
                for row in labels
            ],
        }

    target_chart = None
    if target_inspection_result and target_inspection_result.get("class_distribution"):
        target_chart = target_distribution_chart(target_inspection_result["class_distribution"])

    return {
        "histograms": histograms,
        "category_counts": category_counts,
        "missing_values_chart": missing_values_chart(data),
        "correlation_heatmap": correlation_heatmap,
        "target_distribution_chart": target_chart,
    }
