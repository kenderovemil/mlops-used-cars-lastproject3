#!/bin/bash

# Azure ML Pipeline Validation Script
# This script validates all components, environments, and data assets before running the pipeline

set -e  # Exit on error

echo "🔍 Azure ML Pipeline Validation Script"
echo "========================================"
echo ""

# Configuration
SUBSCRIPTION_ID="77c91b3f-d78c-4832-8ed2-a5dd9c501e0e"
RESOURCE_GROUP="streaming_autovehicle_pricing_MLOPS"
WORKSPACE_NAME="project_III_MLOPS"

echo "📌 Using Configuration:"
echo "   Subscription: $SUBSCRIPTION_ID"
echo "   Resource Group: $RESOURCE_GROUP"
echo "   Workspace: $WORKSPACE_NAME"
echo ""

# Check Azure CLI
echo "✓ Checking Azure CLI..."
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first."
    exit 1
fi
echo "  Azure CLI version: $(az --version | head -n 1)"
echo ""

# Check ML extension
echo "✓ Checking Azure ML extension..."
if ! az extension list | grep -q "ml"; then
    echo "⚠️  Azure ML extension not found. Installing..."
    az extension add -n ml -y
else
    echo "  Azure ML extension installed"
fi
echo ""

# Login check
echo "✓ Checking Azure authentication..."
if ! az account show &> /dev/null; then
    echo "❌ Not logged in to Azure. Please run: az login"
    exit 1
fi
echo "  Logged in successfully"
echo ""

# Set subscription
echo "✓ Setting active subscription..."
az account set --subscription $SUBSCRIPTION_ID
echo "  Active subscription: $(az account show --query name -o tsv)"
echo ""

# Validate workspace
echo "✓ Validating workspace..."
if ! az ml workspace show --name $WORKSPACE_NAME --resource-group $RESOURCE_GROUP &> /dev/null; then
    echo "❌ Workspace '$WORKSPACE_NAME' not found"
    exit 1
fi
echo "  Workspace validated: $WORKSPACE_NAME"
echo ""

# Check compute
echo "✓ Checking compute targets..."
echo "  Available compute:"
az ml compute list --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME --query "[].{Name:name, Type:type, State:provisioning_state}" -o table
echo ""

# Check environments
echo "✓ Checking environments..."
echo "  Looking for: skycore-train-env-used-cars-mlops-v3:13"
if az ml environment show --name skycore-train-env-used-cars-mlops-v3 --version 13 \
   --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME &> /dev/null; then
    echo "  ✅ Environment found: skycore-train-env-used-cars-mlops-v3:13"
else
    echo "  ⚠️  Environment not found. Available environments:"
    az ml environment list --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME \
       --query "[?contains(name, 'skycore') || contains(name, 'used-cars')].{Name:name, Version:version}" -o table
fi
echo ""

# Check data assets
echo "✓ Checking data assets..."
echo "  Looking for: used_cars_raw:1"
if az ml data show --name used_cars_raw --version 1 \
   --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME &> /dev/null; then
    echo "  ✅ Data asset found: used_cars_raw:1"
else
    echo "  ⚠️  Data asset not found. Available data assets:"
    az ml data list --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME \
       --query "[?contains(name, 'used') || contains(name, 'cars')].{Name:name, Version:version, Type:type}" -o table
fi
echo ""

# Register components
echo "✓ Registering/Updating components..."

# Register prep component
echo "  Registering prep_component..."
if az ml component create --file mlops/azureml/train/prep.yml \
   --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME; then
    echo "  ✅ prep_component:3 registered"
else
    echo "  ⚠️  Failed to register prep_component"
fi

# Register train component
echo "  Registering train_model_component..."
if az ml component create --file mlops/azureml/train/train.yml \
   --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME; then
    echo "  ✅ train_model_component:3 registered"
else
    echo "  ⚠️  Failed to register train_model_component"
fi

# Register register component
echo "  Registering register_component..."
if az ml component create --file mlops/azureml/train/register.yml \
   --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME; then
    echo "  ✅ register_component:3 registered"
else
    echo "  ⚠️  Failed to register register_component"
fi
echo ""

# List all components
echo "✓ Listing registered components..."
az ml component list --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME \
   --query "[?contains(name, 'prep') || contains(name, 'train') || contains(name, 'register')].{Name:name, Version:version}" -o table
echo ""

# Validate pipeline YAML
echo "✓ Validating pipeline YAML files..."
for pipeline in mlops/azureml/train/newpipeline.yml mlops/azureml/train/full_pipeline_skycore_clean.yml; do
    if [ -f "$pipeline" ]; then
        echo "  Checking: $pipeline"
        if python3 -c "import yaml; yaml.safe_load(open('$pipeline'))" 2>/dev/null; then
            echo "  ✅ Valid YAML syntax"
        else
            echo "  ❌ Invalid YAML syntax"
        fi
    fi
done
echo ""

echo "========================================"
echo "✅ Validation Complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. If any components are missing, run:"
echo "     az ml component create --file <component.yml> --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME"
echo ""
echo "  2. To test the pipeline, run:"
echo "     az ml job create --file mlops/azureml/train/newpipeline.yml --resource-group $RESOURCE_GROUP --workspace-name $WORKSPACE_NAME"
echo ""
echo "  3. To submit via GitHub Actions:"
echo "     git add ."
echo "     git commit -m 'Fix pipeline configuration'"
echo "     git push"
echo ""
