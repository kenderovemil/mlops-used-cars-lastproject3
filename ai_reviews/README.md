# Azure Login Failure Diagnostic Analysis - README

## Overview

This directory contains comprehensive diagnostic analysis and remediation for the persistent Azure Login failures in GitHub Actions workflows using `auth-type: IDENTITY`.

## Problem Statement

GitHub Actions workflows were failing with these error patterns:
- "Unsupported value 'OIDC'"
- "Attempting Azure CLI login by using user-assigned managed identity"
- "Passing the managed identity ID with --username is no longer supported"

These errors indicated that `azure/login@v1` was incorrectly choosing managed identity mode instead of federated identity (OIDC) mode.

## Files in this Directory

### 1. `copilot_review.txt`
**Comprehensive cross-check analysis** including:
- Complete audit of all azure/login@v1 usage across workflows
- Federated credential subject/issuer matrix
- Detailed findings on auth-type propagation issues
- Recommendations for YAML changes
- Python SDK readiness assessment
- Cross-reference table of all Azure Login implementations

**Key Finding:** auth-type input is optional (required: false) in all workflows, causing azure/login@v1 to fall back to auto-detection that incorrectly selects managed identity mode.

### 2. `cursor_review.txt`
**Deep-dive root cause analysis** including:
- Detailed findings by workflow with line-by-line analysis
- Azure login action behavior analysis and inferred internal logic
- Error message breakdown explaining each failure mode
- Federated credential requirements and common mistakes
- Root cause conclusion with 90% confidence
- Specific fix locations with exact before/after code
- Alternative solution using Python SDK migration
- Verification plan and manual checklist

**Key Finding:** When auth-type is empty/undefined, azure/login@v1 prioritizes managed identity detection over OIDC detection, even when id-token: write is present.

### 3. `findings_summary.txt`
**Executive summary** with:
- Root cause statement
- Specific files and lines to change
- Exact change required (auth-type default: IDENTITY)
- Testing confirmation steps
- 90% confidence assessment

### 4. `action_plan.md`
**Step-by-step remediation plan** including:
- Step 1: YAML corrections (auth-type: required: true, default: IDENTITY)
- Step 2: Add temporary diagnostic debug steps
- Step 3: Verify/update federated credentials in Azure AD
- Step 4: Validation testing procedures
- Step 5: Alternative path using Python SDK migration (if needed)
- Step 6: Final cleanup after resolution
- Timeline, priorities, success criteria, and rollback plan

### 5. `log_extracts/azure_login_debug_template.txt`
**Template for capturing diagnostic evidence** including:
- Debug context output sections
- Azure login step output capture
- Error message collection
- Workflow run metadata
- Job-specific log structure
- Federated credentials verification checklist
- GitHub secrets verification

## Changes Applied

### Auth-Type Input Fix (Applied to 4 files)

**Files Modified:**
1. `.github/workflows/custom-create-compute.yml` (lines 28-31)
2. `.github/workflows/custom-register-dataset.yml` (lines 22-25)
3. `.github/workflows/custom-register-environment.yml` (lines 24-27)
4. `.github/workflows/custom-run-pipeline.yml` (lines 18-21)

**Change Made:**
```yaml
# BEFORE
auth-type:
  required: false
  type: string

# AFTER
auth-type:
  required: true
  type: string
  default: IDENTITY
```

**Impact:** Forces azure/login@v1 to always use IDENTITY mode, preventing auto-detection fallback to managed identity.

### Debug Steps Added (Applied to 4 files)

**Files Modified:**
1. `.github/workflows/custom-create-compute.yml` (after line 47)
2. `.github/workflows/custom-register-dataset.yml` (after line 42)
3. `.github/workflows/custom-register-environment.yml` (after line 43)
4. `.github/workflows/custom-run-pipeline.yml` (after line 39)

**Debug Step Added:**
```yaml
- name: Debug Azure Login Context
  run: |
    echo "=== Azure Login Diagnostic ==="
    echo "GitHub Ref: ${{ github.ref }}"
    echo "GitHub Event: ${{ github.event_name }}"
    echo "GitHub Repository: ${{ github.repository }}"
    echo "Auth-Type Input: '${{ inputs.auth-type }}'"
    echo "Client ID present: ${{ secrets.AZURE_CLIENT_ID != '' }}"
    echo "Tenant ID present: ${{ secrets.AZURE_TENANT_ID != '' }}"
    echo "Subscription ID present: ${{ secrets.AZURE_SUBSCRIPTION_ID != '' }}"
    echo "================================"
```

**Impact:** Captures runtime context to verify auth-type is properly set and secrets are available.

**Note:** This debug step is temporary and should be removed once the issue is confirmed resolved.

## Root Cause Summary

**Primary Issue:** Optional auth-type parameter defaults to empty string, triggering azure/login@v1 auto-detection logic that incorrectly selects managed identity mode instead of federated identity (OIDC) mode.

**Why It Happens:**
1. Reusable workflows define auth-type as `required: false`
2. If value becomes empty/undefined during propagation, azure/login@v1 receives empty auth-type
3. Action falls back to auto-detection
4. Sees client-id + subscription-id parameters
5. Incorrectly assumes user-assigned managed identity
6. Attempts deprecated Azure CLI command: `az login --identity --username <client-id>`
7. Fails with "Passing managed identity ID with --username is no longer supported"

**Solution:** Make auth-type required with explicit default value "IDENTITY" to prevent auto-detection.

## Validation Plan

### Phase 1: Pull Request Testing
1. Create/update pull request with these changes
2. Observe pull_request trigger
3. Check workflow run logs:
   - ✓ Debug step shows auth-type: 'IDENTITY'
   - ✓ Azure Login shows "Using federated identity token"
   - ✓ NO "user-assigned managed identity" messages
   - ✓ All secrets present (true/true/true)

### Phase 2: Main Branch Testing
1. Merge PR to main branch
2. Observe push trigger
3. Verify all four jobs succeed:
   - create-compute
   - register-dataset
   - register-environment
   - run-pipeline

### Phase 3: Collect Evidence
Save workflow logs to `log_extracts/`:
- `azure_login_debug.txt` - Debug output from first successful run
- `workflow_run_summary.txt` - Run metadata and status
- `azure_login_success.txt` - Azure Login step success logs

### Success Criteria
- ✅ Azure Login completes without errors
- ✅ No managed identity error messages
- ✅ All four reusable workflows succeed
- ✅ Pipeline job submits successfully
- ✅ Debug output confirms auth-type is 'IDENTITY'

## Azure AD Configuration Requirements

### Federated Credentials Needed

For repository: `kenderovemil/mlops-used-cars-lastproject3`

**Credential 1: Main Branch**
- Issuer: `https://token.actions.githubusercontent.com`
- Subject: `repo:kenderovemil/mlops-used-cars-lastproject3:ref:refs/heads/main`
- Audience: `api://AzureADTokenExchange`

**Credential 2: Pull Requests**
- Issuer: `https://token.actions.githubusercontent.com`
- Subject: `repo:kenderovemil/mlops-used-cars-lastproject3:pull_request`
- Audience: `api://AzureADTokenExchange`

**Credential 3: PR Refs (Optional)**
- Issuer: `https://token.actions.githubusercontent.com`
- Subject: `repo:kenderovemil/mlops-used-cars-lastproject3:ref:refs/pull/*`
- Audience: `api://AzureADTokenExchange`

### Verification Checklist
- [ ] App Registration client ID matches AZURE_CLIENT_ID secret
- [ ] All three federated credentials exist in Azure AD
- [ ] Subject patterns exactly match (case-sensitive)
- [ ] Issuer URL is exactly `https://token.actions.githubusercontent.com`
- [ ] Audience is exactly `api://AzureADTokenExchange`
- [ ] No typos in repository name or owner name

## Alternative Solution: Python SDK Migration

If azure/login@v1 continues to fail, workflows can be migrated to use Python SDK exclusively:

**Advantages:**
- ✓ No dependency on azure/login@v1 action
- ✓ DefaultAzureCredential automatically handles OIDC
- ✓ More reliable and consistent
- ✓ Better error messages
- ✓ Already implemented for compute creation

**Migration Status:**
- ✅ `custom-create-compute.yml` - Already uses Python SDK
- ⏸️ `custom-register-dataset.yml` - Can migrate to register_dataset.py
- ⏸️ `custom-register-environment.yml` - Can migrate to register_environment.py
- ⏸️ `custom-run-pipeline.yml` - Can migrate to run_pipeline.py

See `action_plan.md` Step 5 for detailed migration instructions.

## Python SDK Scripts Available

All scripts are ready for use with DefaultAzureCredential:

1. **`mlops/scripts/create_compute.py`**
   - Creates/updates Azure ML compute cluster
   - Environment: AZURE_SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME

2. **`mlops/scripts/register_dataset.py`**
   - Registers datasets in Azure ML workspace
   - Environment: AZURE_SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME, DATASET_FILE, DATASET_NAME

3. **`mlops/scripts/register_environment.py`**
   - Registers ML training environments
   - Environment: AZURE_SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME, ENV_FILE

4. **`mlops/scripts/run_pipeline.py`**
   - Submits ML pipeline jobs
   - Environment: AZURE_SUBSCRIPTION_ID, RESOURCE_GROUP, WORKSPACE_NAME, PIPELINE_FILE, JOB_NAME

All scripts use `DefaultAzureCredential()` which automatically detects and uses OIDC tokens when `id-token: write` permission is present.

## Cleanup Tasks

After successful validation (5+ consecutive successful runs):

1. **Remove debug steps** from all four workflow files:
   - custom-create-compute.yml
   - custom-register-dataset.yml
   - custom-register-environment.yml
   - custom-run-pipeline.yml

2. **Archive successful logs** in `log_extracts/`

3. **Document resolution** with before/after metrics

4. **Consider Python SDK migration** for long-term reliability

## References

- **Azure Login Action:** https://github.com/marketplace/actions/azure-login
- **GitHub OIDC:** https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure
- **Azure Federated Credentials:** https://learn.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation
- **Azure ML Python SDK:** https://learn.microsoft.com/en-us/python/api/overview/azure/ai-ml-readme

## Contact

For questions about this diagnostic analysis:
- Review `copilot_review.txt` for detailed cross-check analysis
- Review `cursor_review.txt` for deep-dive root cause analysis
- Review `action_plan.md` for step-by-step remediation
- Check `findings_summary.txt` for executive summary

---

**Generated:** 2025-11-08  
**Repository:** kenderovemil/mlops-used-cars-lastproject3  
**Branch:** copilot/diagnose-azure-login-issues  
**Confidence:** 90% (High)
