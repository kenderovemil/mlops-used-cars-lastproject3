from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_data
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

    # Register dataset from YAML definition
    dataset_file = os.environ.get("DATASET_FILE", "mlops/azureml/train/data.yml")
    dataset_name = os.environ.get("DATASET_NAME", "used-cars-data")

    # Load the data asset from YAML file
    data_asset = load_data(source=dataset_file)
    ml_client.data.create_or_update(data_asset)
    print(f"✅ Dataset '{dataset_name}' registered successfully")
except AzureError as e:
    print(f"❌ Azure API error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
