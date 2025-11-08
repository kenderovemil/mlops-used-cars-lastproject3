from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_job
import os

credential = DefaultAzureCredential()

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
resource_group = os.environ["RESOURCE_GROUP"]
workspace_name = os.environ["WORKSPACE_NAME"]

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
