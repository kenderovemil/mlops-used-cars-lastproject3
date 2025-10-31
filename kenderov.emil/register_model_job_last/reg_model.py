import argparse
import mlflow
import mlflow.sklearn
import joblib
import pandas as pd
from mlflow.models.signature import infer_signature

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str)
    parser.add_argument("--train_data", type=str)
    args = parser.parse_args()

    model_path = args.model
    train_path = args.train_data
    model_name = "used_cars_price_prediction_model"
    artifact_path = "random_forest_price_regressor"

    # Зареждане на модела и тренировъчните данни
    model = joblib.load(model_path)
    train_df = pd.read_csv(train_path)

    X_train = train_df.drop("price", axis=1)
    y_train = train_df["price"]

    # Инфериране на signature
    signature = infer_signature(X_train, model.predict(X_train))

    with mlflow.start_run():
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path=artifact_path,
            registered_model_name=model_name,
            signature=signature
        )
        print(f"✅ Model registered in MLflow as '{model_name}'")

if __name__ == "__main__":
    main()

