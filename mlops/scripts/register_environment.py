from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_environment
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

env_file = os.environ.get("ENV_FILE", "mlops/azureml/train/train-env.yml")

# Load the environment from YAML file
environment = load_environment(source=env_file)
ml_client.environments.create_or_update(environment)
print("✅ Environment registered successfully")
