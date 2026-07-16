from src.data_insight_engine import generate_data_insights
from src.prediction_engine import run_prediction_engine
from src.autopsy_engine import run_autopsy


FILE_PATH = "data/Telco-Customer-Churn.csv"
TARGET_COLUMN = "Churn"


# --------------------------------------------------
# DATA INSIGHT ENGINE
# --------------------------------------------------

insight_result = generate_data_insights(FILE_PATH, target_column=TARGET_COLUMN)
dataset_summary = insight_result["dataset_summary"]

print("\n--- DATA INSIGHT ENGINE: DATASET SUMMARY ---")

print("Total rows:", dataset_summary["total_rows"])
print("Total columns:", dataset_summary["total_columns"])
print("Numeric columns:", dataset_summary["numeric_columns"])
print("Categorical columns:", dataset_summary["categorical_columns"])
print("Total missing values:", dataset_summary["total_missing_values"])
print("Columns with missing values:", dataset_summary["columns_with_missing_values"])
print("Duplicate rows:", dataset_summary["duplicate_rows"])
print("Numeric text columns converted:", dataset_summary["converted_numeric_columns"])

print("\n--- COLUMN METADATA ---")
for column in insight_result["column_metadata"]:
    print(
        f"  {column['column']:<20} dtype={column['dtype']:<10} "
        f"type={column['inferred_type']:<20} "
        f"missing={column['missing_count']:<5} "
        f"unique={column['unique_count']}"
    )

print("\n--- NUMERIC COLUMN ANALYSIS ---")
for column, stats in insight_result["numeric_analysis"].items():
    print(f"\n  {column}")
    for key, value in stats.items():
        print(f"    {key}: {value}")

print("\n--- BINARY NUMERIC COLUMN ANALYSIS ---")
for column, stats in insight_result["binary_analysis"].items():
    print(f"\n  {column}")
    print("    count:", stats["count"])
    print("    missing_count:", stats["missing_count"])
    print("    missing_percentage:", stats["missing_percentage"])
    print("    values:", stats["values"])

print("\n--- CATEGORICAL COLUMN ANALYSIS (first 3 columns shown in full) ---")
for i, (column, stats) in enumerate(insight_result["categorical_analysis"].items()):
    if i < 3:
        print(f"\n  {column}")
        print("    number_of_categories:", stats["number_of_categories"])
        print("    most_common_value:", stats["most_common_value"])
        print("    least_common_value:", stats["least_common_value"])
        print("    top_categories:", stats["top_categories"])
    else:
        print(f"  {column}: {stats['number_of_categories']} categories, most common = {stats['most_common_value']}")

print("\n--- DATA QUALITY ---")
data_quality = insight_result["data_quality"]
print("Duplicate rows:", data_quality["duplicate_rows"])
print("Constant columns:", data_quality["constant_columns"])
print("Near-constant columns:", data_quality["near_constant_columns"])
print("Possible ID columns:", data_quality["possible_id_columns"])
print("Numeric-looking text columns:", data_quality["numeric_looking_text_columns"])
print("High cardinality columns:", data_quality["high_cardinality_columns"])
print("Low variance numeric columns:", data_quality["low_variance_numeric_columns"])
print("\nQuality warnings:")
for warning in data_quality["warnings"]:
    print("  -", warning)

print("\n--- CORRELATION ANALYSIS ---")
correlation_analysis = insight_result["correlation_analysis"]
print("Available:", correlation_analysis["available"])
print("Threshold:", correlation_analysis["threshold"])
print("Strong positive pairs:", correlation_analysis["strong_positive_pairs"])
print("Strong negative pairs:", correlation_analysis["strong_negative_pairs"])
print("Note:", correlation_analysis["note"])

print("\n--- TARGET COLUMN INSPECTION ---")
target_inspection = insight_result["target_inspection"]
for key, value in target_inspection.items():
    print(f"  {key}: {value}")

print("\n--- CHART-READY DATA (shapes only, not full arrays) ---")
chart_data = insight_result["chart_data"]
print("Histograms generated for:", list(chart_data["histograms"].keys()))
print("Category charts generated for:", list(chart_data["category_counts"].keys()))
print("Missing values chart columns:", len(chart_data["missing_values_chart"]["columns"]))
print("Correlation heatmap available:", chart_data["correlation_heatmap"] is not None)
print("Target distribution chart available:", chart_data["target_distribution_chart"] is not None)

print("\n--- AUTOMATIC INSIGHTS ---")
for insight in insight_result["insights"]:
    print("  -", insight)


# --------------------------------------------------
# PREDICTION ENGINE
# --------------------------------------------------

prediction_result = run_prediction_engine(FILE_PATH, TARGET_COLUMN)

print("\n--- PREDICTION ENGINE ---")

print("Prediction Engine completed!")
print("Model:", prediction_result["model_name"])
print("Model Accuracy:", prediction_result["accuracy"] * 100, "%")
print("Training samples:", prediction_result["training_samples"])
print("Testing samples:", prediction_result["testing_samples"])
print("Possible ID columns excluded:", prediction_result["possible_id_columns"])
print("Numeric text columns converted:", prediction_result["converted_numeric_columns"])

for warning in prediction_result["warnings"]:
    print("WARNING:", warning)


# --------------------------------------------------
# MODEL AUTOPSY
# --------------------------------------------------

autopsy_result = run_autopsy(
    prediction_result["X_test"],
    prediction_result["y_test"],
    prediction_result["y_pred"],
    numeric_feature_names=prediction_result["numeric_feature_names"],
)

print("\n--- MODEL AUTOPSY ---")

print("Number of wrong predictions:", autopsy_result["number_of_errors"])

if not autopsy_result["has_errors"]:
    print(autopsy_result["summary"])

else:
    print("\nMost common confusion patterns:")
    for pattern, count in autopsy_result["confusion_patterns"].items():
        print(" ", pattern, ":", count)

    dominant = autopsy_result["dominant_failure"]

    print("\n--- BIGGEST FAILURE PATTERN ---")
    print("Actual class:", dominant["actual_class"])
    print("Predicted class:", dominant["predicted_class"])
    print("Number of failures:", dominant["count"])
    print("Percentage of total errors:", round(dominant["percentage_of_errors"], 2), "%")

    print("\n--- TOP FEATURE DIFFERENCES (numeric - standardized mean difference) ---")
    for item in autopsy_result["feature_differences"]["numeric"][:10]:
        if item["value"] is None:
            print(" ", item["feature"], ": undefined (zero variance, means differ) -", item["note"])
        else:
            print(" ", item["feature"], ":", round(item["value"], 4))

    print("\n--- TOP FEATURE DIFFERENCES (categorical - percentage-point difference) ---")
    for item in autopsy_result["feature_differences"]["categorical"][:10]:
        print(" ", item["feature"], ":", round(item["value"], 2), "percentage points")

    print("\n--- AUTOMATIC AUTOPSY SUMMARY ---")
    print(autopsy_result["summary"])


# --------------------------------------------------
# CLASS PERFORMANCE
# --------------------------------------------------

print("\n--- CLASS PERFORMANCE ---")

class_performance = autopsy_result["class_performance"]

for class_name, metrics in class_performance.items():

    if class_name in ["accuracy", "macro avg", "weighted avg"]:
        continue

    print("\nClass:", class_name)
    print("Precision:", round(metrics["precision"] * 100, 2), "%")
    print("Recall:", round(metrics["recall"] * 100, 2), "%")
    print("F1 Score:", round(metrics["f1-score"] * 100, 2), "%")
    print("Support:", metrics["support"])


# --------------------------------------------------
# WEAK CLASS DETECTION
# --------------------------------------------------

print("\n--- WEAK CLASS DETECTION ---")

weak_classes = autopsy_result["weak_classes"]

if weak_classes:
    for class_name, metrics in weak_classes.items():
        print("\nWARNING: Weak class detected")
        print("Class:", class_name)
        print("Recall:", round(metrics["recall"] * 100, 2), "%")
        print("Support:", metrics["support"])
else:
    print("No weak classes detected.")
