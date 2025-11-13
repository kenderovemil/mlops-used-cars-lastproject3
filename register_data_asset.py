#!/usr/bin/env python3
"""
Register data asset version 2 with accessible local file path
"""
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Data
from azure.ai.ml.constants import AssetTypes
from azure.identity import DefaultAzureCredential

# Azure ML Workspace details
subscription_id = "77c91b3f-d78c-4832-8ed2-a5dd9c501e0e"
resource_group = "streaming_autovehicle_pricing_MLOPS"
workspace_name = "project_III_MLOPS"

# Initialize MLClient
credential = DefaultAzureCredential()
ml_client = MLClient(
    credential=credential,
    subscription_id=subscription_id,
    resource_group_name=resource_group,
    workspace_name=workspace_name
)

# Define data asset from local file
data_asset = Data(
    name="used_cars_raw",
    version="2",
    description="Used cars raw data - registered from local file",
    path="mlops/azureml/train/used_cars_raw.csv",
    type=AssetTypes.URI_FILE,
)

# Register the data asset
print("Registering data asset used_cars_raw:2...")
registered_data = ml_client.data.create_or_update(data_asset)
print(f"✓ Data asset registered: {registered_data.name}:{registered_data.version}")
print(f"  Path: {registered_data.path}")
print(f"\nNow update newpipeline.yml to use version 2:")
print(f"  data_asset: azureml:used_cars_raw:2")
