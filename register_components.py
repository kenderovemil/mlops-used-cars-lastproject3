"""
Component Registration Script for Azure ML Pipeline
Registers all components with the correct versions and validates configuration
"""

from azure.ai.ml import MLClient
from azure.ai.ml import load_component
from azure.identity import DefaultAzureCredential
import os
import sys

# Configuration
SUBSCRIPTION_ID = "77c91b3f-d78c-4832-8ed2-a5dd9c501e0e"
RESOURCE_GROUP = "streaming_autovehicle_pricing_MLOPS"
WORKSPACE_NAME = "project_III_MLOPS"

def main():
    print("🔧 Azure ML Component Registration Script")
    print("=" * 50)
    print()
    
    # Initialize ML Client
    print("📌 Connecting to Azure ML Workspace...")
    try:
        ml_client = MLClient(
            DefaultAzureCredential(),
            subscription_id=SUBSCRIPTION_ID,
            resource_group_name=RESOURCE_GROUP,
            workspace_name=WORKSPACE_NAME
        )
        print(f"✅ Connected to workspace: {WORKSPACE_NAME}")
    except Exception as e:
        print(f"❌ Failed to connect to workspace: {e}")
        sys.exit(1)
    
    print()
    
    # Component files to register
    components = {
        "prep_component": "mlops/azureml/train/prep.yml",
        "train_model_component": "mlops/azureml/train/train.yml",
        "register_component": "mlops/azureml/train/register.yml"
    }
    
    registered_components = []
    failed_components = []
    
    # Register each component
    for component_name, component_path in components.items():
        print(f"📦 Registering {component_name}...")
        
        if not os.path.exists(component_path):
            print(f"   ❌ File not found: {component_path}")
            failed_components.append(component_name)
            continue
        
        try:
            component = load_component(source=component_path)
            registered = ml_client.components.create_or_update(component)
            print(f"   ✅ Registered: {registered.name}:{registered.version}")
            registered_components.append(f"{registered.name}:{registered.version}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            failed_components.append(component_name)
    
    print()
    print("=" * 50)
    print("📊 Registration Summary:")
    print(f"   ✅ Successful: {len(registered_components)}")
    print(f"   ❌ Failed: {len(failed_components)}")
    print()
    
    if registered_components:
        print("✅ Successfully registered components:")
        for comp in registered_components:
            print(f"   - {comp}")
        print()
    
    if failed_components:
        print("❌ Failed to register:")
        for comp in failed_components:
            print(f"   - {comp}")
        print()
        sys.exit(1)
    
    # Validate environment exists
    print("🔍 Validating environment...")
    try:
        env = ml_client.environments.get(
            name="skycore-train-env-used-cars-mlops-v3",
            version="13"
        )
        print(f"   ✅ Environment found: {env.name}:{env.version}")
    except Exception as e:
        print(f"   ⚠️  Environment not found: {e}")
        print("   Please ensure the environment is registered before running the pipeline.")
    
    print()
    
    # Validate data asset
    print("🔍 Validating data asset...")
    try:
        data = ml_client.data.get(name="used_cars_raw", version="1")
        print(f"   ✅ Data asset found: {data.name}:{data.version}")
    except Exception as e:
        print(f"   ⚠️  Data asset not found: {e}")
        print("   Please register the data asset before running the pipeline.")
    
    print()
    print("=" * 50)
    print("✅ Component registration complete!")
    print()
    print("📋 Next steps:")
    print("   1. Validate pipeline YAML files")
    print("   2. Test pipeline submission:")
    print(f"      az ml job create --file mlops/azureml/train/newpipeline.yml \\")
    print(f"        --resource-group {RESOURCE_GROUP} \\")
    print(f"        --workspace-name {WORKSPACE_NAME}")
    print()

if __name__ == "__main__":
    main()
