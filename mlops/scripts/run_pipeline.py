from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_job
from azure.core.exceptions import AzureError
import os
import sys
from utils import load_credentials

# Load credentials from JSON file
load_credentials()

# Check for required environment variables
required = ["AZURE_SUBSCRIPTION_ID", "RESOURCE_GROUP", "WORKSPACE_NAME"]
for var in required:
    if not os.environ.get(var):
        raise ValueError(f"Missing environment variable: {var}")

credential = DefaultAzureCredential()

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group = os.environ["RESOURCE_GROUP"]
workspace_name = os.environ["WORKSPACE_NAME"]

try:
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )

    pipeline_file = os.environ.get("PIPELINE_FILE", "mlops/azureml/train/newpipeline.yml")
    job_name = os.environ.get("JOB_NAME", "mlops-pipeline")

    # Load the job from YAML file
    job = load_job(source=pipeline_file)
    submitted_job = ml_client.jobs.create_or_update(job)
    print(f"✅ Pipeline job '{job_name}' submitted successfully")
    print(f"Job name: {submitted_job.name}")
except AzureError as e:
    print(f"❌ Azure API error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
