from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute
from azure.core.exceptions import AzureError
import os
import sys
from pathlib import Path

# Add parent directory to path to import config module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from mlops.config import load_credentials

# Load credentials from JSON file
load_credentials()

# Check for required environment variables
required = ["AZURE_SUBSCRIPTION_ID", "RESOURCE_GROUP", "WORKSPACE_NAME"]
for var in required:
    if not os.environ.get(var):
        raise ValueError(f"Missing environment variable: {var}")

# Credentials via OIDC (GitHub Actions)
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

    cpu_cluster = AmlCompute(
        name="cpu-cluster",
        size="Standard_DS11_v2",
        min_instances=0,
        max_instances=1,
        tier="dedicated"
    )

    ml_client.compute.begin_create_or_update(cpu_cluster).result()
    print("✅ Compute cluster created or updated successfully")
except AzureError as e:
    print(f"❌ Azure API error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
