#!/usr/bin/env python3
import argparse, os, sys, json, traceback
from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn

def parse_args():
    parser = argparse.ArgumentParser(description="Train Random Forest Regressor")
    parser.add_argument("--train_data", required=True, help="Path to training CSV")
    parser.add_argument("--test_data", required=True, help="Path to testing CSV")
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=None)
    parser.add_argument("--model_output", required=True, help="Directory to save MLflow model")
    return parser.parse_args()

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def write_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        print(f"[DEBUG] Diagnostics written to: {path}", flush=True)
    except Exception as e:
        print(f"[WARN] Failed to write diagnostics: {e}", flush=True)

def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    df = pd.read_csv(path)
    if df.shape[0] == 0:
        raise ValueError("CSV contains zero rows")
    return df

def main():
    args = parse_args()
    print(f"[DEBUG] Parsed args: {vars(args)}", flush=True)

    try:
        df_train = load_data(args.train_data)
        df_test = load_data(args.test_data)

        X_train = df_train.drop("price", axis=1)
        y_train = df_train["price"]
        X_test = df_test.drop("price", axis=1)
        y_test = df_test["price"]

        model = RandomForestRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=42
        )

        mlflow.start_run()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)

        mlflow.log_param("n_estimators", args.n_estimators)
        mlflow.log_param("max_depth", args.max_depth)
        mlflow.log_metric("mse", mse)
        mlflow.sklearn.log_model(model, artifact_path="model")

        ensure_dir(args.model_output)
        mlflow.sklearn.save_model(model, args.model_output)

        diagnostics = {
            "status": "completed",
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "train_rows": df_train.shape[0],
            "test_rows": df_test.shape[0],
            "n_estimators": args.n_estimators,
            "max_depth": args.max_depth,
            "mse": mse,
            "model_output": args.model_output
        }
        write_json(os.path.join(args.model_output, "train_diagnostics.json"), diagnostics)

        print(f"✅ Model trained. MSE: {mse:.4f}", flush=True)
        mlflow.end_run()
        sys.exit(0)

    except Exception as e:
        traceback.print_exc()
        write_json(".", {"status": "failed", "exception": str(e)})
        sys.exit(1)

if __name__ == "__main__":
    main()
