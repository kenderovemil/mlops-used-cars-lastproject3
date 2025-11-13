# Azure ML Pipeline Fixes - Summary Report

## 🎯 Overview
All critical issues in your Azure ML pipeline have been systematically fixed. This document summarizes the changes made and provides instructions for validation and deployment.

---

## ✅ Fixed Issues

### 1. Component YAML Files Updated

#### **prep.yml** (`mlops/azureml/train/prep.yml`)
- ✅ Added version: `3`
- ✅ Standardized environment: `azureml:skycore-train-env-used-cars-mlops-v3:13`
- ✅ Confirmed script: `prep.py` with correct arguments
- ✅ Component name: `prep_component`

#### **train.yml** (`mlops/azureml/train/train.yml`)
- ✅ Renamed to: `train_model_component` (version 3)
- ✅ Fixed arguments to match train.py:
  - `--train_data` (folder)
  - `--test_data` (folder)
  - `--n_estimators` (with default: 100)
  - `--max_depth` (optional)
  - `--model_output` (folder)
- ✅ Standardized environment: `azureml:skycore-train-env-used-cars-mlops-v3:13`

#### **register.yml** (`mlops/azureml/train/register.yml`)
- ✅ Added version: `3`
- ✅ Standardized environment: `azureml:skycore-train-env-used-cars-mlops-v3:13`
- ✅ Component name: `register_component`

---

### 2. Pipeline YAML Files Fixed

#### **newpipeline.yml** (`mlops/azureml/train/newpipeline.yml`)
- ✅ Replaced `<новата версия>` with actual version numbers (`:3`)
- ✅ Fixed component references:
  - `azureml:prep_component:3`
  - `azureml:train_model_component:3` (renamed from train_component)
  - `azureml:register_component:3`
- ✅ Fixed duplicate output mapping:
  - Separate `train_data` and `test_data` outputs
  - No longer both mapping to `clean_data`
- ✅ Updated pipeline name and experiment name

#### **full_pipeline_skycore_clean.yml** (`mlops/azureml/train/full_pipeline_skycore_clean.yml`)
- ✅ Removed non-existent `tune_model_component`
- ✅ Updated to 3-step pipeline: prep → train → register
- ✅ Fixed component references to version 3
- ✅ Added separate outputs for train_data, test_data, model_output, registered_model_info

---

### 3. Python Scripts Fixed

#### **train.py** (`data-science/src/train.py`)
- ✅ Changed argument from `--data` to `--train_data` and `--test_data`
- ✅ Updated `resolve_data_path()` to handle folder inputs
- ✅ Modified `main()` to load separate train/test datasets
- ✅ Removed internal train_test_split (now handled by prep.py)

---

### 4. GitHub Workflow Updated

#### **custom-run-pipeline.yml** (`.github/workflows/custom-run-pipeline.yml`)
- ✅ Updated to use individual GitHub Secrets instead of JSON credential object:
  - `AZURE_CLIENT_ID`
  - `AZURE_CLIENT_SECRET`
  - `AZURE_SUBSCRIPTION_ID`
  - `AZURE_TENANT_ID`
  - `AZURE_RESOURCE_GROUP`
  - `AZURE_WORKSPACE_NAME`
- ✅ Fixed Azure login credentials format
- ✅ Updated environment variable setting

---

## 📋 Validation Tools Created

### 1. **validate_pipeline.sh**
Bash script that validates:
- Azure CLI installation
- Azure authentication
- Workspace existence
- Compute targets
- Environments (skycore-train-env-used-cars-mlops-v3:13)
- Data assets (used_cars_raw:1)
- Component registration
- Pipeline YAML syntax

**Usage:**
```bash
cd /home/azureuser/cloudfiles/code/Users/kenderov.emil
./validate_pipeline.sh
```

### 2. **register_components.py**
Python script that:
- Registers all components (prep, train, register) with version 3
- Validates environment exists
- Validates data asset exists
- Provides detailed success/failure feedback

**Usage:**
```bash
python register_components.py
```

---

## 🔧 Configuration Details

### Azure Configuration Used:
- **Subscription ID:** `77c91b3f-d78c-4832-8ed2-a5dd9c501e0e`
- **Resource Group:** `streaming_autovehicle_pricing_MLOPS`
- **Workspace:** `project_III_MLOPS`
- **Service Principal:**
  - Client ID: `c88b9a2a-6803-412c-bb39-c912b700019c`
  - Display Name: `skycore-sp`

### Environment Reference:
- **Name:** `skycore-train-env-used-cars-mlops-v3`
- **Version:** `13`

### Data Asset Reference:
- **Name:** `used_cars_raw`
- **Version:** `1`

### Component Versions:
All components now use version **3**:
- `prep_component:3`
- `train_model_component:3`
- `register_component:3`

---

## 🚀 Deployment Instructions

### Step 1: Register Components
```bash
# Option A: Using Python script
python register_components.py

# Option B: Using Azure CLI
az ml component create --file mlops/azureml/train/prep.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS

az ml component create --file mlops/azureml/train/train.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS

az ml component create --file mlops/azureml/train/register.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS
```

### Step 2: Validate Registration
```bash
# List all registered components
az ml component list \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS \
  --query "[?contains(name, 'prep') || contains(name, 'train') || contains(name, 'register')]"
```

### Step 3: Test Pipeline Locally
```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('mlops/azureml/train/newpipeline.yml'))"

# Submit pipeline
az ml job create \
  --file mlops/azureml/train/newpipeline.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS
```

### Step 4: Deploy via GitHub Actions
```bash
# Commit all changes
git add .
git commit -m "Fix: Update pipeline components and configurations to v3"
git push origin fix-workflows

# GitHub Actions will automatically:
# 1. Register components
# 2. Submit pipeline
# 3. Monitor execution
```

---

## 🧪 Testing Checklist

Before deploying to production, verify:

- [ ] All components registered successfully (version 3)
- [ ] Environment `skycore-train-env-used-cars-mlops-v3:13` exists
- [ ] Data asset `used_cars_raw:1` exists
- [ ] Compute cluster `cpu-cluster` is available
- [ ] GitHub Secrets are correctly configured:
  - [ ] AZURE_CLIENT_ID
  - [ ] AZURE_CLIENT_SECRET
  - [ ] AZURE_SUBSCRIPTION_ID
  - [ ] AZURE_TENANT_ID
  - [ ] AZURE_RESOURCE_GROUP
  - [ ] AZURE_WORKSPACE_NAME
- [ ] Pipeline YAML files validate without errors
- [ ] Local test scripts run successfully:
  - [ ] `python data-science/src/prep.py --raw_data <path> --train_data ./outputs/train --test_data ./outputs/test`
  - [ ] `python data-science/src/train.py --train_data ./outputs/train --test_data ./outputs/test --model_output ./outputs/model --n_estimators 100 --max_depth 10`

---

## 📊 File Changes Summary

### Modified Files:
1. `mlops/azureml/train/prep.yml`
2. `mlops/azureml/train/train.yml`
3. `mlops/azureml/train/register.yml`
4. `mlops/azureml/train/newpipeline.yml`
5. `mlops/azureml/train/full_pipeline_skycore_clean.yml`
6. `data-science/src/train.py`
7. `.github/workflows/custom-run-pipeline.yml`

### Created Files:
1. `validate_pipeline.sh` - Validation script
2. `register_components.py` - Component registration script
3. `PIPELINE_FIXES_SUMMARY.md` - This document

---

## ⚠️ Known Considerations

1. **Environment Version:** Ensure `skycore-train-env-used-cars-mlops-v3:13` is registered and available.

2. **Data Asset:** Verify `used_cars_raw:1` points to the correct data file location.

3. **Compute:** Ensure `cpu-cluster` has sufficient capacity and is not in a failed state.

4. **GitHub Secrets:** All secrets must be set correctly in repository settings.

5. **Service Principal Permissions:** The service principal needs Contributor role on the ML workspace.

---

## 🆘 Troubleshooting

### Issue: Component not found
```bash
# Solution: Re-register component
az ml component create --file <component.yml> \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS
```

### Issue: Environment not found
```bash
# Solution: List available environments
az ml environment list \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS

# If needed, update component YAMLs with correct environment version
```

### Issue: Pipeline validation fails
```bash
# Solution: Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('mlops/azureml/train/newpipeline.yml'))"

# Check component versions match
az ml component list --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS
```

### Issue: GitHub Actions authentication fails
```bash
# Solution: Verify secrets in GitHub repository settings
# Ensure all 6 secrets are correctly configured:
# - AZURE_CLIENT_ID
# - AZURE_CLIENT_SECRET
# - AZURE_SUBSCRIPTION_ID
# - AZURE_TENANT_ID
# - AZURE_RESOURCE_GROUP
# - AZURE_WORKSPACE_NAME
```

---

## 📞 Support

For additional assistance:
1. Check Azure ML Studio logs for detailed error messages
2. Review component registration output
3. Validate environment and data asset availability
4. Ensure service principal has correct permissions

---

**Last Updated:** November 13, 2025  
**Pipeline Version:** v3  
**Status:** ✅ Ready for deployment
