
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

def write_diagnostics(args, mse, r2, model_path):
    #log_path = "/mnt/batch/tasks/shared/LS_root/mounts/clusters/lastprojectcompute/code/Users/kenderov.emil/notes/notes/train_diagnostics.txt"
    log_path = os.path.join(args.model_output, "train_diagnostics.txt")

    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            f.write("=== TRAIN MODEL DIAGNOSTICS ===\n")
            f.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n\n")

            f.write(">>> ARGUMENTS:\n")
            f.write(json.dumps(vars(args), indent=2))
            f.write("\n\n")

            f.write(">>> ENVIRONMENT VARIABLES (partial):\n")
            env = {k: v for k, v in os.environ.items() if "AZUREML" in k or "ML" in k}
            f.write(json.dumps(env, indent=2))
            f.write("\n\n")

            f.write(">>> METRICS:\n")
            f.write(f"MSE: {mse:.4f}\n")
            f.write(f"R2: {r2:.4f}\n\n")

            f.write(">>> MODEL OUTPUT PATH:\n")
            f.write(f"{model_path}\n")
            if os.path.exists(model_path):
                f.write("📂 Contents:\n")
                for item in os.listdir(model_path):
                    f.write(f" - {item}\n")
            else:
                f.write("❌ model_output path does not exist.\n")

            f.write("\n=== END ===\n")
    except Exception as e:
        print(f"⚠️ Failed to write diagnostics: {e}", flush=True)

def main(args):
    # Зареждане на данните
    print("🚀 train.py started", flush=True)
    train_df = pd.read_csv(os.path.join(args.train_data, "train.csv"))
    test_df = pd.read_csv(os.path.join(args.test_data, "test.csv"))
    print(f"✅ Train shape: {train_df.shape}, Test shape: {test_df.shape}", flush=True)
    X_train = train_df.drop("price", axis=1)
    y_train = train_df["price"]
    X_test = test_df.drop("price", axis=1)
    y_test = test_df["price"]

    # Определяне на категориални и числови колони
    categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns
    numeric_cols = X_train.select_dtypes(exclude=["object", "category"]).columns

    # Преобразувания
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("numeric", StandardScaler(), numeric_cols)
        ]
    )

    # Pipeline: preprocessing + модел
    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=args.n_estimators,
            max_depth=args.max_depth,
            random_state=42
        ))
    ])

    # Трениране
    model.fit(X_train, y_train)

    # Предсказване и метрики
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"✅ MSE: {mse}, R2: {r2}", flush=True)
    print(f"##metric_name:MSE", flush=True)
    print(f"##metric_value:{mse}", flush=True)

    print("🏁 train.py finished", flush=True)
    # Запазване на модела
    os.makedirs(args.model_output, exist_ok=True)
    model_path = os.path.join(args.model_output, "model.pkl")
    joblib.dump(model, model_path)

    # Запис на метриките
    metrics_path = os.path.join(args.model_output, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump({"MSE": mse, "R2": r2}, f)

    print(f"✅ Model trained. MSE={mse:.4f}, R2={r2:.4f}")

    # Диагностика
    write_diagnostics(args, mse, r2, args.model_output)
    with open(os.path.join(args.model_output, "metrics.txt"), "w") as f:
        f.write(f"MSE: {mse}\nR2: {r2}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_data", type=str)
    parser.add_argument("--test_data", type=str)
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=None)
    parser.add_argument("--model_output", type=str)
    args = parser.parse_args()
    main(args)
    



# import argparse
# import os
# import pandas as pd
# import joblib
# import json

# from sklearn.compose import ColumnTransformer
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error, r2_score


# def main(args):
#     # Зареждане на данните
#     train_df = pd.read_csv(os.path.join(args.train_data, "train.csv"))
#     test_df = pd.read_csv(os.path.join(args.test_data, "test.csv"))

#     X_train = train_df.drop("price", axis=1)
#     y_train = train_df["price"]
#     X_test = test_df.drop("price", axis=1)
#     y_test = test_df["price"]

#     # Определяне на категориални и числови колони
#     categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns
#     numeric_cols = X_train.select_dtypes(exclude=["object", "category"]).columns

#     # Преобразувания
#     preprocessor = ColumnTransformer(
#         transformers=[
#             ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
#             ("numeric", StandardScaler(), numeric_cols)
#         ]
#     )

#     # Pipeline: preprocessing + модел
#     model = Pipeline(steps=[
#         ("preprocessor", preprocessor),
#         ("regressor", RandomForestRegressor(
#             n_estimators=args.n_estimators,
#             max_depth=args.max_depth,
#             random_state=42
#         ))
#     ])

#     # Трениране
#     model.fit(X_train, y_train)

#     # Предсказване и метрики
#     preds = model.predict(X_test)
#     mse = mean_squared_error(y_test, preds)
#     r2 = r2_score(y_test, preds)

#     # Запазване на модела локално в изходната папка
#     os.makedirs(args.model_output, exist_ok=True)
#     model_path = os.path.join(args.model_output, "model.pkl")
#     joblib.dump(model, model_path)

#     # Запис на метриките в JSON файл
#     metrics_path = os.path.join(args.model_output, "metrics.json")
#     with open(metrics_path, "w") as f:
#         json.dump({"MSE": mse, "R2": r2}, f)

#     print(f"✅ Model trained. MSE={mse:.4f}, R2={r2:.4f}")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--train_data", type=str)
#     parser.add_argument("--test_data", type=str)
#     parser.add_argument("--n_estimators", type=int, default=100)
#     parser.add_argument("--max_depth", type=int, default=None)
#     parser.add_argument("--model_output", type=str)
#     args = parser.parse_args()
#     main(args)
