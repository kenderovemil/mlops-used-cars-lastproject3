from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_data
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
    credential = DefaultAzureCredential()

    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )

    # Регистрация на dataset от YAML дефиниция
    dataset_file = os.environ.get("DATASET_FILE", "mlops/azureml/train/data.yml")
    dataset_name = os.environ.get("DATASET_NAME", "used-cars-data")

    # Зареждане на data asset от YAML файл
    data_asset = load_data(source=dataset_file)
    ml_client.data.create_or_update(data_asset)
    print(f"✅ Dataset '{dataset_name}' registered successfully")

except AzureError as e:
    print(f"❌ Azure API error: {e}", flush=True)
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}", flush=True)
    sys.exit(1)

