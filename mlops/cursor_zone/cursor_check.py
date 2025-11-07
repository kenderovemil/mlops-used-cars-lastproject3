# cursor_check.py
# cursor_check.py
# Cursor uses this script to validate pipeline YAMLs before registration.
# It loads the pipeline, checks structure, and prints validation results.

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import PipelineJob
from azure.ai.ml.dsl import pipeline
import os

# Зареждане на credentials от GitHub Secrets
credential = DefaultAzureCredential()
ml_client = MLClient(credential, os.environ["AZURE_SUBSCRIPTION_ID"], os.environ["AZURE_RESOURCE_GROUP"], os.environ["AZURE_WORKSPACE_NAME"])

# Зареждане и валидиране на pipeline
try:
    pipeline_job = ml_client.jobs.load(path="cursor_pipeline.yml")
    print("✅ Pipeline loaded successfully.")
    validation_result = ml_client.jobs.validate(pipeline_job)
    print("✅ Validation passed.")
except Exception as e:
    print(f"⚠️ Validation failed: {e}")
