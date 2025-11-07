import argparse
import joblib
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Model
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--model", type=str, required=True)
args = parser.parse_args()

model_path = Path(args.model) / "best_model.pkl"
print(f"📥 Registering model from: {model_path}")

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="77c91b3f-d78c-4832-8ed2-a5dd9c501e0e",
    resource_group_name="streaming_autovehicle_pricing_MLOPS",
    workspace_name="project_iii_mlops"
)

registered_model = Model(
    path=str(model_path),
    name="final_model",
    type="mlflow_model",
    description="Best tuned model",
)

ml_client.models.create_or_update(registered_model)
print("✅ Model registered successfully.")
