from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute
import os

# Credentials via OIDC (GitHub Actions)
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

cpu_cluster = AmlCompute(
    name="cpu-cluster",
    size="Standard_DS11_v2",
    min_instances=0,
    max_instances=1,
    tier="dedicated"
)

ml_client.begin_create_or_update(cpu_cluster)
print("✅ Compute cluster created or updated successfully")
