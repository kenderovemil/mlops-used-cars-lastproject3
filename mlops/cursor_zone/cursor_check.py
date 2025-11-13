# cursor_check.py
# Cursor uses this script to validate pipeline YAMLs before registration.
# It loads the pipeline, checks structure, and prints validation results.

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os
import sys

# Зареждане на credentials от environment variables с fallback към дефолтни стойности
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "77c91b3f-d78c-4832-8ed2-a5dd9c501e0e")
resource_group = os.environ.get("AZURE_RESOURCE_GROUP", "streaming_autovehicle_pricing_MLOPS")
workspace_name = os.environ.get("AZURE_WORKSPACE_NAME", "project_III_MLOPS")

try:
    credential = DefaultAzureCredential()
    ml_client = MLClient(
        credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )

    # Зареждане и валидиране на pipeline
    pipeline_job = ml_client.jobs.load(path="cursor_pipeline.yml")
    print("✅ Pipeline loaded successfully.")

    validation_result = ml_client.jobs.validate(pipeline_job)
    print("✅ Validation passed.")

except Exception as e:
    print(f"⚠️ Validation failed: {e}", flush=True)
    sys.exit(1)
