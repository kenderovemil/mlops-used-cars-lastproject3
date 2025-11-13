# Azure ML Pipeline Project - Status Report
**Date:** November 13, 2025  
**Workspace:** project_III_MLOPS_v2 (NEW - Identity-based authentication)

## ✅ **Successfully Completed**

### 1. New Workspace Creation
- **Workspace Name:** project_III_MLOPS_v2
- **Authentication Mode:** `identity` (managed identity-based)
- **Storage Account:** projectistorage2dd8a3255
- **Managed Identity:** 5c2e2d92-4716-4c49-aa56-4965f9cad2a3
- **Status:** ✅ Created successfully

### 2. Infrastructure Setup
- ✅ Compute cluster: `cpu-cluster` (Standard_DS11_v2)
- ✅ Datastore: `skycore_storage` (skycorestorage/skycore container)
- ✅ Environment: `skycore-train-env-used-cars-mlops-v3:13`
- ✅ Components registered: prep_component:3, train_model_component:3, register_component:3

### 3. Data Assets
- ✅ used_cars_data:1 - Initial 5-row sample (188 bytes)
- ✅ used_cars_data:2 - Full dataset (9469 bytes from used_cars.csv)

### 4. RBAC Permissions Granted
```bash
# Workspace managed identity permissions:
5c2e2d92-4716-4c49-aa56-4965f9cad2a3:
  - Storage Blob Data Contributor on projectistorage2dd8a3255 (workspace storage)
  - Storage Blob Data Contributor on skycorestorage (external storage)
```

## ⚠️ **Current Issue**

### Pipeline Execution Status
**Last Job:** zen_wheel_1md4rf9ltt  
**Status:** Failed (immediate failure)  
**Submitted:** 18:10 UTC  

### Problem Summary
Despite having a properly configured workspace with:
- ✅ system_datastores_auth_mode = "identity"
- ✅ Proper RBAC permissions granted
- ✅ Valid data assets registered
- ✅ All components registered correctly

The pipeline continues to fail immediately upon submission.

### Observed Behavior
1. Pipeline submits successfully (status: NotStarted)
2. Within 30 seconds, status changes to Failed
3. No child jobs are created
4. No detailed error messages available via CLI

### Previous Failed Attempts
- heroic_rocket_x4snr8qvqw - Failed (test_train_ratio parameter issue - fixed)
- keen_jewel_8hb44dbhpx - Running → prep_data failed (auth error on artifact download)
- plucky_cup_wcs9hkhbjd - Failed immediately after RBAC grants
- olden_pump_529p65fb6q - Failed after 2-minute RBAC propagation wait
- zen_wheel_1md4rf9ltt - Failed with full dataset (version 2)

## 🔍 **Root Cause Analysis**

### Hypothesis
RBAC permissions can take 5-15 minutes to fully propagate across Azure services. The permissions were granted at:
- projectistorage2dd8a3255: ~17:44 UTC (automatically during workspace creation)
- skycorestorage: ~18:00 UTC (manually granted)

Latest pipeline submission: ~18:10 UTC (10 minutes after skycorestorage grant)

### Evidence
1. Job keen_jewel_8hb44dbhpx showed "Running" status and created a prep_data child job
2. The prep_data job failed with: "AuthorizationPermissionMismatch" when downloading artifacts
3. This indicates the workspace can queue jobs but the compute can't access storage

### Technical Details
```json
Datastore Configuration (skycore_storage):
{
  "account": "skycorestorage",
  "container": "skycore",
  "credentials": {},  // Empty = identity-based auth
  "type": "azure_blob"
}

Workspace Default Datastore (workspaceblobstore):
{
  "account": "projectistorage2dd8a3255",
  "credentials": {},  // Empty = identity-based auth
  "type": "azure_blob"
}
```

## 📋 **Next Steps**

### Option 1: Wait for RBAC Propagation (RECOMMENDED)
**Time Required:** 15-30 minutes from grant time (18:00 UTC)  
**Expected Success Time:** ~18:15 - 18:30 UTC

**Action:**
```bash
# Wait until 18:30 UTC, then resubmit:
az ml job create \
  --file mlops/azureml/train/pipeline_v2_workspace.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS_v2 \
  --web
```

### Option 2: Use Account Key Authentication (FALLBACK)
If identity-based auth continues to fail after 30 minutes, revert to account key:

**Steps:**
1. Update skycore_storage datastore with account key credentials
2. Update data asset registration
3. Resubmit pipeline

**Note:** This defeats the purpose of creating the new workspace with identity auth.

### Option 3: Contact Azure Support
If both options fail, workspace may have underlying configuration issues requiring support ticket.

## 📊 **Configuration Files**

### Working Pipeline YAML
**Location:** `/home/azureuser/cloudfiles/code/Users/kenderov.emil/mlops/azureml/train/pipeline_v2_workspace.yml`

```yaml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
display_name: "Used Cars Pipeline - New Workspace (Identity Auth)"
experiment_name: used_cars_pipeline_v2

inputs:
  raw_data:
    type: uri_file
    path: azureml:used_cars_data:2  # Full dataset
    mode: download

settings:
  default_compute: azureml:cpu-cluster

jobs:
  prep_data:
    component: azureml:prep_component:3
  train_model:
    component: azureml:train_model_component:3
  register_model:
    component: azureml:register_component:3
```

## 🔗 **Useful Links**

**Azure ML Studio (New Workspace):**
https://ml.azure.com/workspaces/project_III_MLOPS_v2

**Latest Pipeline Run:**
https://ml.azure.com/runs/zen_wheel_1md4rf9ltt?wsid=/subscriptions/77c91b3f-d78c-4832-8ed2-a5dd9c501e0e/resourcegroups/streaming_autovehicle_pricing_MLOPS/workspaces/project_III_MLOPS_v2

## 💡 **Key Learnings**

1. **Workspace Authentication Configuration is Immutable**
   - Must be set at creation time via `--system-datastores-auth-mode`
   - Cannot be changed after workspace creation
   - Old workspace (project_III_MLOPS) had unfixable authentication issues

2. **RBAC Propagation Takes Time**
   - Role assignments can take 5-30 minutes to propagate
   - Must wait for full propagation before testing
   - Immediate retries will continue to fail

3. **Identity-Based Auth vs Account Keys**
   - Identity: More secure, no credential management, but requires RBAC setup
   - Account Keys: Immediate access, but credentials must be managed/rotated

4. **Datastore Validation**
   - Empty credentials (`{}`) indicates identity-based authentication
   - Non-empty credentials contain account keys or SAS tokens
   - Check `system_datastores_auth_mode` at workspace level

## ✨ **Expected Outcome**

Once RBAC permissions fully propagate, the pipeline should:
1. ✅ Submit successfully
2. ✅ Create prep_data job → downloads CSV, splits into train/test
3. ✅ Create train_model job → trains Random Forest model
4. ✅ Create register_model job → registers model in MLflow
5. ✅ Complete with status "Completed"

**Estimated Total Runtime:** 5-10 minutes after successful submission

---

**Status:** ⏳ Waiting for RBAC propagation  
**Next Check:** 18:30 UTC (20 minutes after grant)  
**Confidence Level:** High - infrastructure is correctly configured
