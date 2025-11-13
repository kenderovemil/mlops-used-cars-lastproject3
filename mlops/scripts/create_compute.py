from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import AmlCompute
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

try:
    # Credentials via OIDC (GitHub Actions) или Managed Identity
    credential = DefaultAzureCredential()

    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )

    # Дефиниране на compute cluster
    cpu_cluster = AmlCompute(
        name="cpu-cluster",
        size="Standard_DS11_v2",
        min_instances=0,
        max_instances=1,
        tier="dedicated"
    )

    # Създаване или обновяване на compute cluster
    ml_client.compute.begin_create_or_update(cpu_cluster).result()
    print("✅ Compute cluster created or updated successfully")

except AzureError as e:
    print(f"❌ Azure API error: {e}", flush=True)
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}", flush=True)
    sys.exit(1)
