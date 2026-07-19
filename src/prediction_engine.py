import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from src.shared.column_typing import (
    convert_numeric_looking_columns,
    detect_possible_id_columns
)


def run_prediction_engine(
    file_path,
    target_column,
    id_uniqueness_threshold=0.90,
    numeric_conversion_threshold=0.90
):

    # Load dataset based on file type
    if file_path.endswith(".csv"):
        data = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        data = pd.read_excel(file_path)

    else:
        raise ValueError("Unsupported file format")

    if target_column not in data.columns:
        raise ValueError(
            f"Target column '{target_column}' was not found in the dataset."
        )

    # Separate input features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]

# Remove unwanted index columns like "Unnamed: 0"
    unnamed_columns = [col for col in X.columns if col.startswith("Unnamed")]
    if unnamed_columns:
        X = X.drop(columns=unnamed_columns)

    # --------------------------------------------------------------
    # SCHEMA-LEVEL STEPS (safe to run before the split)
    #
    # These decide what TYPE each column is (numeric vs text) and
    # whether a column looks like an identifier. Neither step fits a
    # statistic that becomes a model input, and neither looks at the
    # target column, so running them on the full dataset does not
    # leak test-set information the way the OLD get_dummies +
    # median-fill-before-split approach did.
    # --------------------------------------------------------------

    text_columns = X.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    converted_numeric_columns = convert_numeric_looking_columns(
        X, text_columns, threshold=numeric_conversion_threshold
    )

    remaining_text_columns = X.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    possible_id_columns = detect_possible_id_columns(
        X, remaining_text_columns, threshold=id_uniqueness_threshold
    )

    # Report the decision instead of silently hiding it
    # (columns are still excluded from modelling by default)
    X = X.drop(columns=possible_id_columns)

    categorical_columns = X.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    numeric_columns = X.select_dtypes(
        include="number"
    ).columns.tolist()

    # Convert all categorical columns to strings
    for column in categorical_columns:
        X[column] = X[column].astype(str)

    if len(categorical_columns) == 0 and len(numeric_columns) == 0:
        raise ValueError(
            "No usable feature columns remain after removing possible ID "
            "columns. Cannot train a model."
        )

    # --------------------------------------------------------------
    # SPLIT BEFORE FITTING ANY PREPROCESSING
    #
    # This is the leakage fix. The OLD code ran get_dummies and
    # median-fill on the full X and only split afterwards, so the
    # median values and one-hot vocabulary were both computed using
    # test rows. Splitting first and fitting preprocessing only on
    # X_train (below) removes that leak.
    # --------------------------------------------------------------

    class_counts = y.value_counts()
    can_stratify = len(class_counts) > 0 and class_counts.min() >= 2

    split_warning = None

    if can_stratify:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
    else:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        split_warning = (
            "Stratified splitting was skipped because at least one class "
            "has fewer than 2 members. A random (non-stratified) split "
            "was used instead, so class proportions between train and "
            "test may differ slightly."
        )

    # --------------------------------------------------------------
    # PREPROCESSING PIPELINE - fit ONLY on training data
    # --------------------------------------------------------------

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", SimpleImputer(strategy="median"), numeric_columns),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                categorical_columns
            ),
        ],
        verbose_feature_names_out=False
    )

    # Keeps transform() output as a DataFrame with readable column names
    # like "Contract_Two year" instead of an unlabelled numpy array.
    preprocessor.set_output(transform="pandas")

    model = RandomForestClassifier(random_state=42)

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model),
    ])

    pipeline.fit(X_train, y_train)

    X_test_transformed = pipeline.named_steps["preprocessor"].transform(X_test)
    y_pred = pipeline.named_steps["model"].predict(X_test_transformed)

    accuracy = accuracy_score(y_test, y_pred)

    # Record which transformed columns are numeric vs one-hot/categorical
    # so the Model Autopsy Engine knows which difference formula to use
    # for each one.
    numeric_feature_names = list(numeric_columns)
    categorical_feature_names = [
        column for column in X_test_transformed.columns
        if column not in numeric_feature_names
    ]

    return {
        "model_name": "RandomForestClassifier",
        "pipeline": pipeline,
        "X_test": X_test_transformed,
        "y_test": y_test,
        "y_pred": y_pred,
        "accuracy": accuracy,
        "training_samples": len(X_train),
        "testing_samples": len(X_test),
        "numeric_feature_names": numeric_feature_names,
        "categorical_feature_names": categorical_feature_names,
        "possible_id_columns": possible_id_columns,
        "converted_numeric_columns": converted_numeric_columns,
        "warnings": [split_warning] if split_warning else [],
    }
