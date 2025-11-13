# 🔍 Storage Authentication Failure - Root Cause Analysis

**Date**: November 13, 2025  
**Pipeline**: brave_soursop_kc9bpdzrd0  
**Status**: Failed with ScriptExecution.StreamAccess.Authentication

---

## 🚨 Root Cause Identified

The pipeline fails because of a **datastore authentication configuration mismatch**:

### Current Configuration Issue:
```
Workspace: project_III_MLOPS
Default Datastore: workspaceblobstore
Storage Account: projectiiimlop4426449596
Authentication Method: Account Key (but credentials are empty/missing)
```

### Evidence:
1. ✅ Workspace Managed Identity has **all required RBAC roles**:
   - Storage Blob Data Contributor ✅
   - Storage Blob Data Reader ✅
   - Storage File Data Privileged Contributor ✅
   - Storage Queue Data Contributor ✅

2. ❌ **Datastore credentials are empty** (`credentials: {}`):
   - This means the workspace is configured for **account key auth**
   - But no account keys are registered in the datastore
   - Even though RBAC permissions exist, they're not being used

3. ❌ **Authentication Mode Mismatch**:
   - Workspace has `system_datastores_auth_mode: accesskey`
   - But should be using `identity` (managed identity) authentication

---

## 🎯 The Problem

When Azure ML tries to:
1. Upload code artifacts to blob storage
2. Download input data
3. Write output results

It attempts to authenticate using **account keys** (the default datastore credential method), but:
- No keys are configured in the datastore
- The managed identity RBAC permissions are being **ignored**
- Authorization header is malformed because there's no valid credential

---

## 💡 Three Solution Paths

### **Option 1: Fix Current Workspace (Recommended - Fastest)**
Update the default datastore to use managed identity authentication:

```bash
# Update workspaceblobstore to use identity auth
az ml datastore update \
  --name workspaceblobstore \
  --workspace-name project_III_MLOPS \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --auth-mode identity
```

**Pros**: 
- Keeps existing workspace
- Leverages existing RBAC permissions
- Quick fix (1 command)

**Cons**: 
- May not work if workspace-level auth mode is locked
- Requires testing

---

### **Option 2: Use Your External Storage (skycorestorage)**
Create a new datastore pointing to your `skycorestorage` account with identity auth:

```bash
# Create new datastore with identity auth
az ml datastore create \
  --name skycore_datastore_identity \
  --type azure_blob \
  --account-name skycorestorage \
  --container-name skycore \
  --workspace-name project_III_MLOPS \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --auth-mode identity
```

Then update pipeline to use this datastore for outputs.

**Pros**: 
- Uses your working storage account
- Clean separation from problematic workspace storage

**Cons**: 
- Requires managed identity to have permissions on skycorestorage
- Need to modify pipeline YAMLs

---

### **Option 3: Create New Workspace (Nuclear Option)**
Start fresh with a new workspace configured correctly from the beginning:

```bash
# Create new workspace with identity-based auth
az ml workspace create \
  --name project_III_MLOPS_v2 \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --system-datastores-auth-mode identity
```

**Pros**: 
- Clean slate
- Properly configured from start
- No legacy configuration issues

**Cons**: 
- Most time-consuming
- Need to re-register all components
- Need to recreate compute cluster

---

## 📋 Recommended Action Plan

### **STEP 1: Try Datastore Update (5 minutes)**
```bash
az ml datastore update \
  --name workspaceblobstore \
  --workspace-name project_III_MLOPS \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --auth-mode identity
```

### **STEP 2: If that fails, use external storage (10 minutes)**
1. Grant workspace MI permissions on skycorestorage
2. Create new identity-based datastore
3. Update pipeline to reference new datastore

### **STEP 3: If both fail, create new workspace (30 minutes)**
1. Create new workspace with `--system-datastores-auth-mode identity`
2. Create compute cluster
3. Re-register components
4. Submit pipeline

---

## 🔧 Why The Embedded Data Approach Failed

Even though we embedded the CSV data in the Python script:
- Azure ML still needs to **upload the code artifacts** (Python scripts) to blob storage
- This upload uses the **default datastore** (workspaceblobstore)
- The upload fails because of the authentication issue
- The job never even starts executing the embedded data code

---

## 📊 Technical Details

**Workspace Managed Identity**: `ba8419e4-3e28-41ab-bcb7-3847930f9e8e`  
**Service Principal**: `c88b9a2a-6803-412c-bb39-c912b700019c` (also has Storage Blob Data Contributor)  
**Storage Account**: `projectiiimlop4426449596`  
**External Storage**: `skycorestorage` (contains skycore container with your data)

**Error Pattern**:
```
PermissionDenied(Some(Server failed to authenticate the request. 
Make sure the value of the Authorization header is formed correctly 
including the signature.))
```

This error signature indicates **account key authentication failure**, not RBAC failure.

---

## ✅ Next Steps

Let me know which option you'd like to pursue:
1. **Quick fix**: Try updating datastore auth mode
2. **External storage**: Use your skycorestorage account
3. **Clean slate**: Create new workspace

I'm ready to execute whichever path you choose! 🚀
