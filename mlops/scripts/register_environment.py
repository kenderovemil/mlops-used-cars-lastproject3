from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient, load_environment
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
    # Вземане на креденшъли (OIDC, Managed Identity или локални)
    credential = DefaultAzureCredential()

    ml_client = MLClient(
        credential=credential,
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name
    )

    # Зареждане и регистриране на средата
    env_file = os.environ.get("ENV_FILE", "mlops/azureml/train/train-env.yml")
    environment = load_environment(source=env_file)
    ml_client.environments.create_or_update(environment)

    print("✅ Environment registered successfully")

except AzureError as e:
    print(f"❌ Azure API error: {e}", flush=True)
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}", flush=True)
    sys.exit(1)
