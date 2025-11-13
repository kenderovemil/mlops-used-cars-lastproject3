#!/bin/bash
# SkyCore Pipeline - New Workspace Setup
# This script creates a fresh workspace with proper authentication configuration

set -e

echo "🚀 Creating new Azure ML workspace with identity-based authentication..."

# Create new workspace
az ml workspace create \
  --name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --location eastus \
  --display-name "Used Cars MLOps - Fixed Authentication" \
  --description "New workspace with proper storage authentication" \
  --system-datastores-auth-mode identity

echo "✅ Workspace created successfully!"

# Create compute cluster
echo "📊 Creating compute cluster..."
az ml compute create \
  --name cpu-cluster \
  --type amlcompute \
  --size Standard_DS11_v2 \
  --min-instances 0 \
  --max-instances 1 \
  --workspace-name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS

echo "✅ Compute cluster created!"

# Create datastore with your skycorestorage
echo "💾 Creating SkyCore datastore..."
cat > /tmp/skycore_datastore.yml << 'EOF'
$schema: https://azuremlschemas.azureedge.net/latest/azureBlobDatastore.schema.json
name: skycore_storage
type: azure_blob
description: "SkyCore external storage"
account_name: skycorestorage
container_name: skycore
credentials:
  account_key: <YOUR_STORAGE_ACCOUNT_KEY_HERE>
EOF

az ml datastore create \
  --file /tmp/skycore_datastore.yml \
  --workspace-name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS

echo "✅ Datastore created!"

# Register data asset
echo "📁 Registering data asset..."
cat > /tmp/data_asset.yml << 'EOF'
$schema: https://azuremlschemas.azureedge.net/latest/data.schema.json
name: used_cars_data
version: "1"
description: "Used cars dataset"
type: uri_file
path: azureml://datastores/skycore_storage/paths/used_cars_raw.csv
EOF

az ml data create \
  --file /tmp/data_asset.yml \
  --workspace-name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS

echo "✅ Data asset registered!"

# Register environment
echo "🐍 Registering environment..."
az ml environment create \
  --file /home/azureuser/cloudfiles/code/Users/kenderov.emil/mlops/azureml/train/train-env.yml \
  --workspace-name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS

echo "✅ Environment registered!"

# Register components
echo "🔧 Registering components..."
az ml component create \
  --file /home/azureuser/cloudfiles/code/Users/kenderov.emil/mlops/azureml/train/prep.yml \
  --workspace-name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS

az ml component create \
  --file /home/azureuser/cloudfiles/code/Users/kenderov.emil/mlops/azureml/train/train.yml \
  --workspace-name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS

az ml component create \
  --file /home/azureuser/cloudfiles/code/Users/kenderov.emil/mlops/azureml/train/register.yml \
  --workspace-name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS

echo "✅ All components registered!"

echo ""
echo "🎉 =========================================="
echo "🎉 NEW WORKSPACE SETUP COMPLETE!"
echo "🎉 =========================================="
echo ""
echo "Workspace: project_III_MLOPS_v2"
echo "Compute: cpu-cluster"
echo "Datastore: skycore_storage"
echo "Data Asset: used_cars_data:1"
echo ""
echo "✅ Ready to submit pipeline!"
