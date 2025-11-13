from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.ai.ml import MLClient, load_job
from azure.core.exceptions import AzureError
import os
import sys
from utils import load_credentials

# Зареждане на креденшъли от JSON файл (ако има такъв)
load_credentials()

# Вземане на конфигурация от environment variables с fallback към дефолтни стойности
subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID", "77c91b3f-d78c-4832-8ed2-a5dd9c501e0e")
resource_group = os.environ.get("RESOURCE_GROUP", "streaming_autovehicle_pricing_MLOPS")
workspace_name = os.environ.get("WORKSPACE_NAME", "project_III_MLOPS")

# Избор на креденшъли: Managed Identity ако е налична, иначе DefaultAzureCredential
try:
    credential = ManagedIdentityCredential()
except Exception:
    credential = DefaultAzureCredential()

try:
    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )

    pipeline_file = os.environ.get("PIPELINE_FILE", "mlops/azureml/train/newpipeline.yml")
    job_name = os.environ.get("JOB_NAME", "mlops-pipeline")

    # Зареждане и стартиране на pipeline job
    job = load_job(source=pipeline_file)
    submitted_job = ml_client.jobs.create_or_update(job)

    print(f"✅ Pipeline job '{job_name}' submitted successfully")
    print(f"Job name: {submitted_job.name}")

except AzureError as e:
    print(f"❌ Azure API error: {e}", flush=True)
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}", flush=True)
    sys.exit(1)

