import pandas as pd
from sklearn.metrics import classification_report


def run_autopsy(X_test, y_test, y_pred, numeric_feature_names=None):
    """
    Compares wrong predictions against correct predictions of the same
    actual class to find the model's dominant failure pattern and which
    features look most different between the two groups.

    numeric_feature_names: names of X_test columns that are continuous
    numeric features (e.g. tenure, MonthlyCharges). Any column NOT in this
    list is treated as a one-hot / binary indicator column, so its group
    means are interpreted as proportions rather than raw numbers. If not
    supplied, columns whose observed values are a subset of {0, 1} are
    auto-detected as binary.
    """

    feature_columns = list(X_test.columns)

    if numeric_feature_names is None:
        numeric_feature_names = [
            column for column in feature_columns
            if set(X_test[column].dropna().unique()) <= {0, 1}
        ]

    numeric_feature_set = set(numeric_feature_names)

    # --------------------------------------------------------------
    # Class-level performance (computed regardless of whether there
    # were any wrong predictions at all)
    # --------------------------------------------------------------

    class_performance = classification_report(
        y_test, y_pred, output_dict=True, zero_division=0
    )

    recall_threshold = 0.60
    weak_classes = {}

    for class_name, metrics in class_performance.items():
        if class_name in ["accuracy", "macro avg", "weighted avg"]:
            continue
        if metrics["recall"] < recall_threshold:
            weak_classes[class_name] = {
                "recall": metrics["recall"],
                "support": metrics["support"],
            }

    wrong_predictions = y_test != y_pred
    correct_predictions = y_test == y_pred

    number_of_errors = int(wrong_predictions.sum())

    # --------------------------------------------------------------
    # GUARD: zero errors - there is no failure pattern to analyse.
    # The OLD code called confusion_patterns.index[0] unconditionally,
    # which raises IndexError here because confusion_patterns would be
    # an empty Series.
    # --------------------------------------------------------------

    if number_of_errors == 0:
        return {
            "number_of_errors": 0,
            "has_errors": False,
            "confusion_patterns": {},
            "dominant_failure": None,
            "feature_differences": {"numeric": [], "categorical": []},
            "summary": (
                "The model made no errors on the test set, so there is no "
                "failure pattern to analyse."
            ),
            "class_performance": class_performance,
            "weak_classes": weak_classes,
        }

    error_data = X_test[wrong_predictions].copy()
    error_data["Actual_Class"] = y_test[wrong_predictions]
    error_data["Predicted_Class"] = y_pred[wrong_predictions]

    correct_data = X_test[correct_predictions].copy()
    correct_data["Actual_Class"] = y_test[correct_predictions]
    correct_data["Predicted_Class"] = y_pred[correct_predictions]

    confusion_patterns = (
        error_data
        .groupby(["Actual_Class", "Predicted_Class"])
        .size()
        .sort_values(ascending=False)
    )

    top_failure_pattern = confusion_patterns.index[0]
    top_actual_class = top_failure_pattern[0]
    top_predicted_class = top_failure_pattern[1]
    top_failure_count = int(confusion_patterns.iloc[0])
    top_failure_percentage = (top_failure_count / number_of_errors) * 100

    top_failure_data = error_data[
        (error_data["Actual_Class"] == top_actual_class)
        & (error_data["Predicted_Class"] == top_predicted_class)
    ]

    correct_class_data = correct_data[
        correct_data["Actual_Class"] == top_actual_class
    ]

    numeric_differences = []
    categorical_differences = []
    feature_note = None

    # --------------------------------------------------------------
    # GUARD: no correctly predicted samples of this class exist, so
    # there is nothing to compare the failures against. The OLD code
    # would silently compute an all-NaN feature_difference here and
    # still report 3 "top" feature names with meaningless scores.
    # --------------------------------------------------------------

    if len(correct_class_data) == 0:
        feature_note = (
            f"No correctly predicted '{top_actual_class}' samples exist to "
            f"compare against, so feature differences could not be "
            f"calculated for this failure pattern."
        )
    else:
        for column in feature_columns:
            failure_values = top_failure_data[column]
            correct_values = correct_class_data[column]

            n1 = len(failure_values)
            n2 = len(correct_values)
            mean1 = float(failure_values.mean())
            mean2 = float(correct_values.mean())

            if column in numeric_feature_set:
                # ---- Standardized mean difference (pooled std) ----
                var1 = failure_values.var(ddof=1) if n1 > 1 else 0.0
                var2 = correct_values.var(ddof=1) if n2 > 1 else 0.0
                var1 = 0.0 if pd.isna(var1) else var1
                var2 = 0.0 if pd.isna(var2) else var2

                degrees_of_freedom = n1 + n2 - 2
                if degrees_of_freedom > 0:
                    pooled_variance = (
                        ((n1 - 1) * var1 + (n2 - 1) * var2) / degrees_of_freedom
                    )
                    pooled_std = pooled_variance ** 0.5
                else:
                    pooled_std = 0.0

                if pooled_std > 1e-8:
                    numeric_differences.append({
                        "feature": column,
                        "metric_type": "standardized_mean_difference",
                        "value": (mean1 - mean2) / pooled_std,
                        "failure_group_mean": mean1,
                        "correct_group_mean": mean2,
                    })
                elif abs(mean1 - mean2) < 1e-8:
                    # Both groups are (near) constant and equal - no
                    # meaningful difference, and no division by zero.
                    numeric_differences.append({
                        "feature": column,
                        "metric_type": "standardized_mean_difference",
                        "value": 0.0,
                        "failure_group_mean": mean1,
                        "correct_group_mean": mean2,
                    })
                else:
                    # Both groups are (near) constant but at different
                    # values - a standardized effect size is undefined
                    # rather than reporting a misleading number.
                    numeric_differences.append({
                        "feature": column,
                        "metric_type": "standardized_mean_difference_undefined",
                        "value": None,
                        "failure_group_mean": mean1,
                        "correct_group_mean": mean2,
                        "note": (
                            "Both groups have ~zero variance but different "
                            "means, so a standardized effect size cannot be "
                            "computed safely."
                        ),
                    })
            else:
                # ---- One-hot / binary feature: means ARE proportions ----
                percentage_point_difference = abs(mean1 - mean2) * 100
                categorical_differences.append({
                    "feature": column,
                    "metric_type": "percentage_point_difference",
                    "value": percentage_point_difference,
                    "failure_group_proportion": mean1,
                    "correct_group_proportion": mean2,
                })

        numeric_differences.sort(
            key=lambda item: abs(item["value"]) if item["value"] is not None else -1,
            reverse=True,
        )
        categorical_differences.sort(key=lambda item: item["value"], reverse=True)

    # --------------------------------------------------------------
    # Build the auto-generated summary
    # --------------------------------------------------------------

    top_numeric_names = [
        item["feature"] for item in numeric_differences[:3]
        if item["value"] is not None
    ]
    top_categorical_names = [
        item["feature"] for item in categorical_differences[:3]
    ]

    summary_parts = [
        f"The dominant failure pattern is {top_actual_class} being "
        f"misclassified as {top_predicted_class}. This pattern occurred "
        f"{top_failure_count} times and accounts for "
        f"{top_failure_percentage:.2f}% of all model errors."
    ]

    if feature_note:
        summary_parts.append(feature_note)
    else:
        if top_numeric_names:
            summary_parts.append(
                "Among numeric features, the largest standardized "
                f"differences between failed and correctly predicted "
                f"{top_actual_class} samples are associated with "
                + ", ".join(top_numeric_names) + "."
            )
        if top_categorical_names:
            summary_parts.append(
                "Among category indicators, the largest proportion "
                "differences are associated with "
                + ", ".join(top_categorical_names) + "."
            )
        summary_parts.append(
            "These are differences associated with the failure pattern, "
            "not proven causes of it."
        )

    autopsy_summary = " ".join(summary_parts)

    return {
        "number_of_errors": number_of_errors,
        "has_errors": True,
        "confusion_patterns": {
            f"{actual} -> {predicted}": int(count)
            for (actual, predicted), count in confusion_patterns.items()
        },
        "dominant_failure": {
            "actual_class": top_actual_class,
            "predicted_class": top_predicted_class,
            "count": top_failure_count,
            "percentage_of_errors": top_failure_percentage,
        },
        "feature_differences": {
            "numeric": numeric_differences,
            "categorical": categorical_differences,
        },
        "summary": autopsy_summary,
        "class_performance": class_performance,
        "weak_classes": weak_classes,
    }
