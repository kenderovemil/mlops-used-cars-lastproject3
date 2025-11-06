import argparse
import os
import json
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import Model
from datetime import datetime

def write_diagnostics(args, log_path):
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w") as f:
            f.write("=== MODEL REGISTRATION DIAGNOSTICS ===\n")
            f.write(f"Timestamp: {datetime.utcnow().isoformat()}Z\n\n")
            f.write(">>> ARGUMENTS:\n")
            f.write(json.dumps(vars(args), indent=2))
            f.write("\n\n")
    except Exception as e:
        print(f"⚠️ Failed to write diagnostics: {e}", flush=True)

def main(args):
    print("🚀 register.py started", flush=True)

    log_path = os.path.join(args.model_info_output_path, "register_diagnostics.txt")
    write_diagnostics(args, log_path)

<<<<<<< HEAD
    ml_client = MLClient(
        DefaultAzureCredential(),
        subscription_id="77c91b3f-d78c-4832-8ed2-a5dd9c501e0e",
        resource_group_name="streaming_autovehicle_pricing_MLOPS",
        workspace_name="project_III_MLOPS"
=======
    # Get configuration from environment variables with fallback to defaults
    subscription_id = os.environ.get("AZUREML_ARM_SUBSCRIPTION", "77c91b3f-d78c-4832-8ed2-a5dd9c501e0e")
    resource_group = os.environ.get("AZUREML_ARM_RESOURCEGROUP", "streaming_autovehicle_pricing_MLOPS")
    workspace_name = os.environ.get("AZUREML_ARM_WORKSPACE_NAME", "project_III_MLOPS")

    ml_client = MLClient(
        DefaultAzureCredential(),
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
>>>>>>> aef2dbfc8c91683f27c0e439296ca79eacd02c7f
    )

    model = Model(
        path=args.model_path,
        name=args.model_name,
        description="Used cars price prediction model"
    )

    registered_model = ml_client.models.create_or_update(model)

    os.makedirs(args.model_info_output_path, exist_ok=True)
    with open(os.path.join(args.model_info_output_path, "model_info.txt"), "w") as f:
        f.write(f"Model name: {registered_model.name}\n")
        f.write(f"Version: {registered_model.version}\n")
        f.write(f"Path: {args.model_path}\n")

    print("🏁 register.py finished", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str)
    parser.add_argument("--model_path", type=str)
    parser.add_argument("--model_info_output_path", type=str)
    args = parser.parse_args()
    main(args)


# import argparse
# from azure.ai.ml import MLClient
# from azure.identity import DefaultAzureCredential
# from azure.ai.ml.entities import Model

# def main(args):
#     ml_client = MLClient(
#         DefaultAzureCredential(),
#         subscription_id="77c91b3f-d78c-4832-8ed2-a5dd9c501e0e",
#         resource_group_name="streaming_autovehicle_pricing_MLOPS",
#         workspace_name="project_III_MLOPS"
#     )

#     model = Model(
#     path=args.model_path,
#     name=args.model_name,
#     description="Used cars price prediction model"
# )



#     registered_model = ml_client.models.create_or_update(model)
#     print(f"✅ Model registered: {registered_model.name}:{registered_model.version}")
    
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--model_name", type=str)
#     parser.add_argument("--model_path", type=str)
#     parser.add_argument("--model_info_output_path", type=str)
#     args = parser.parse_args()
#     main(args)