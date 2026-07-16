"""
Turns already-calculated statistics into one deterministic list of
beginner-friendly sentences. Nothing in this file invents a fact - every
sentence pulls from a number computed elsewhere in the engine.
"""

WIDE_DISTRIBUTION_CV_THRESHOLD = 0.50


def _wide_distribution_columns(numeric_analysis):
    """
    A numeric column is flagged as 'wide' when its standard deviation is
    large relative to its mean (coefficient of variation). This is a
    heuristic for 'spread out', not a statistical guarantee.
    """
    wide_columns = []
    for column, stats in numeric_analysis.items():
        mean = stats.get("mean")
        std = stats.get("standard_deviation")
        if mean and std and abs(mean) > 1e-8:
            if abs(std / mean) > WIDE_DISTRIBUTION_CV_THRESHOLD:
                wide_columns.append(column)
    return wide_columns


def _binary_column_insights(binary_analysis):
    """
    One descriptive sentence per binary numeric column, built directly
    from its computed value breakdown - no coefficient-of-variation or
    "wide distribution" language, since neither applies to a two-valued
    column.
    """
    sentences = []
    for column, stats in binary_analysis.items():
        values = stats.get("values", [])
        if len(values) != 2:
            continue
        first, second = values
        sentences.append(
            f"{column} is a binary numeric column: {first['percentage']}% of rows "
            f"are {first['value']} and {second['percentage']}% are {second['value']}."
        )
    return sentences


def generate_insights(
    dataset_summary,
    data_quality,
    correlation_analysis,
    numeric_analysis,
    binary_analysis,
    target_inspection_result,
):
    insights = []

    total_rows = dataset_summary["total_rows"]
    total_columns = dataset_summary["total_columns"]

    if total_rows == 0:
        insights.append("The dataset has no rows to analyse.")
        return insights

    row_word = "row" if total_rows == 1 else "rows"
    column_word = "column" if total_columns == 1 else "columns"
    insights.append(
        f"The dataset contains {total_rows:,} {row_word} and {total_columns} {column_word}."
    )

    if total_rows == 1:
        insights.append(
            "The dataset has only 1 row, so measures like variance, "
            "correlation, and 'constant column' detection are not "
            "meaningful yet."
        )

    # Data quality warnings are already deterministic sentences - reuse
    # them directly instead of re-deriving the same facts twice.
    insights.extend(data_quality["warnings"])

    for column in _wide_distribution_columns(numeric_analysis):
        insights.append(f"{column} has a wide distribution relative to its average value.")

    insights.extend(_binary_column_insights(binary_analysis))

    if correlation_analysis.get("available"):
        strong_pairs = (
            correlation_analysis["strong_positive_pairs"]
            + correlation_analysis["strong_negative_pairs"]
        )
        if strong_pairs:
            pair_text = ", ".join(
                f"{pair['column_a']} and {pair['column_b']}" for pair in strong_pairs[:3]
            )
            insights.append(
                "The dataset contains highly correlated numeric variables, "
                f"including {pair_text}. This indicates association, not causation."
            )

    if target_inspection_result and not target_inspection_result.get("error"):
        target_column = target_inspection_result["target_column"]

        if target_inspection_result["classification_suitable"] is False:
            insights.append(target_inspection_result["recommendation"])
        elif target_inspection_result["imbalance_level"] in ("moderate", "severe"):
            distribution = target_inspection_result["class_distribution"]
            majority_class = max(distribution, key=lambda c: distribution[c]["count"])
            insights.append(
                f"The target column '{target_column}' is "
                f"{target_inspection_result['imbalance_level']}ly imbalanced - "
                f"'{majority_class}' makes up "
                f"{distribution[majority_class]['percentage']}% of rows."
            )

    return insights
