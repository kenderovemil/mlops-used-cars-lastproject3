from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_environment
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

    env_file = os.environ.get("ENV_FILE", "mlops/azureml/train/train-env.yml")

    # Load the environment from YAML file
    environment = load_environment(source=env_file)
    ml_client.environments.create_or_update(environment)
    print("✅ Environment registered successfully")
except AzureError as e:
    print(f"❌ Azure API error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
