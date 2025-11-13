
import argparse
import os
import pandas as pd
import joblib
import json
from datetime import datetime
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

def write_diagnostics(args, mse, r2):
    log_path = os.path.join(args.model_output, "train_diagnostics.txt")
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            f.write("=== TRAIN MODEL DIAGNOSTICS ===\n")
            f.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n\n")
            f.write(">>> ARGUMENTS:\n")
            f.write(json.dumps(vars(args), indent=2))
            f.write("\n\n")
            f.write(">>> METRICS:\n")
            f.write(f"MSE: {mse:.4f}\n")
            f.write(f"R2: {r2:.4f}\n\n")
    except Exception as e:
        print(f"⚠️ Failed to write diagnostics: {e}", flush=True)

def resolve_data_path(data_arg: str) -> str:
    """Resolve dataset path for AzureML or local runs."""
    if data_arg is None:
        raise ValueError("❌ No data argument provided. Please specify a dataset path.")

    # If it's a directory (AzureML mounts inputs as dirs), pick first CSV
    if os.path.isdir(data_arg):
        files = [f for f in os.listdir(data_arg) if f.endswith(".csv")]
        if not files:
            raise ValueError(f"❌ No CSV files found in directory: {data_arg}")
        return os.path.join(data_arg, files[0])

    # If it's a file path
    if os.path.isfile(data_arg):
        return data_arg

    # If it's a URL (SAS link)
    if data_arg.startswith("http"):
        return data_arg

    raise ValueError(f"❌ Invalid dataset path: {data_arg}")

def main(args):
    print("🚀 train.py started", flush=True)

    # Load train and test data
    train_path = resolve_data_path(args.train_data)
    test_path = resolve_data_path(args.test_data)
    print(f"📂 Loading train data from: {train_path}", flush=True)
    print(f"📂 Loading test data from: {test_path}", flush=True)

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    print(f"✅ Train dataset shape: {train_df.shape}", flush=True)
    print(f"✅ Test dataset shape: {test_df.shape}", flush=True)

    if "price" not in train_df.columns:
        raise ValueError("❌ Train dataset must contain a 'price' column as target variable.")
    if "price" not in test_df.columns:
        raise ValueError("❌ Test dataset must contain a 'price' column as target variable.")

    X_train = train_df.drop("price", axis=1)
    y_train = train_df["price"]
    X_test = test_df.drop("price", axis=1)
    y_test = test_df["price"]

    categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns
    numeric_cols = X_train.select_dtypes(exclude=["object", "category"]).columns

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("numeric", StandardScaler(), numeric_cols)
        ]
    )

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=42
        ))
    ])

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"✅ MSE: {mse:.4f}, R2: {r2:.4f}", flush=True)

    os.makedirs(args.model_output, exist_ok=True)
    model_path = os.path.join(args.model_output, "model.pkl")
    joblib.dump(model, model_path)

    with open(os.path.join(args.model_output, "metrics.json"), "w") as f:
        json.dump({"MSE": mse, "R2": r2}, f)

    write_diagnostics(args, mse, r2)
    print("🏁 train.py finished", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_data", type=str, help="Path to train data folder", required=True)
    parser.add_argument("--test_data", type=str, help="Path to test data folder", required=True)
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=None)
    parser.add_argument("--model_output", type=str, required=True)
    args = parser.parse_args()
    main(args)
