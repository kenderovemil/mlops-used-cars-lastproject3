# Action Plan: Fix Azure Login Failures in GitHub Actions

## Step 1: Apply YAML Corrections to Auth-Type Input

### 1.1 Update custom-create-compute.yml
**File:** `.github/workflows/custom-create-compute.yml`  
**Lines:** 28-30

**Current:**
```yaml
      auth-type:
        required: false
        type: string
```

**New:**
```yaml
      auth-type:
        required: true
        type: string
        default: IDENTITY
```

### 1.2 Update custom-register-dataset.yml
**File:** `.github/workflows/custom-register-dataset.yml`  
**Lines:** 22-24

**Apply same change as 1.1**

### 1.3 Update custom-register-environment.yml
**File:** `.github/workflows/custom-register-environment.yml`  
**Lines:** 24-26

**Apply same change as 1.1**

### 1.4 Update custom-run-pipeline.yml
**File:** `.github/workflows/custom-run-pipeline.yml`  
**Lines:** 18-20

**Apply same change as 1.1**

**Rationale:**
- Ensures `auth-type` is always explicitly set to `IDENTITY`
- Prevents azure/login@v1 from entering auto-detection mode
- Eliminates the managed identity fallback that causes failures

---

## Step 2: Add Temporary Diagnostic Debug Steps

### 2.1 Add debug step to custom-create-compute.yml
**File:** `.github/workflows/custom-create-compute.yml`  
**Insert after:** Line 46 (after checkout)  
**Insert before:** Line 48 (before Azure Login)

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

### 2.2 Add debug step to custom-register-dataset.yml
**File:** `.github/workflows/custom-register-dataset.yml`  
**Insert after:** Line 41 (after checkout)  
**Insert before:** Line 43 (before Azure Login)

**Use same debug step as 2.1**

### 2.3 Add debug step to custom-register-environment.yml
**File:** `.github/workflows/custom-register-environment.yml`  
**Insert after:** Line 42 (after checkout)  
**Insert before:** Line 44 (before Azure Login)

**Use same debug step as 2.1**

### 2.4 Add debug step to custom-run-pipeline.yml
**File:** `.github/workflows/custom-run-pipeline.yml`  
**Insert after:** Line 38 (after checkout)  
**Insert before:** Line 40 (before Azure Login)

**Use same debug step as 2.1**

**Rationale:**
- Captures runtime context for verification
- Confirms auth-type value is correctly propagated
- Verifies secrets are present
- Helps validate federated credential subject matching
- Can be removed once issue is resolved

---

## Step 3: Verify/Update Federated Credentials in Azure AD

### 3.1 Verify App Registration
1. Log into Azure Portal
2. Navigate to **Azure Active Directory** → **App Registrations**
3. Find the App Registration used for GitHub Actions
4. Verify **Application (client) ID** matches `AZURE_CLIENT_ID` secret in GitHub

### 3.2 Check Federated Credentials
Navigate to **Certificates & secrets** → **Federated credentials**

Ensure these three credentials exist:

#### Credential 1: Main Branch Push
- **Name:** `github-main-branch` (or similar)
- **Issuer:** `https://token.actions.githubusercontent.com`
- **Subject:** `repo:kenderovemil/mlops-used-cars-lastproject3:ref:refs/heads/main`
- **Audience:** `api://AzureADTokenExchange`

#### Credential 2: Pull Requests
- **Name:** `github-pull-requests` (or similar)
- **Issuer:** `https://token.actions.githubusercontent.com`
- **Subject:** `repo:kenderovemil/mlops-used-cars-lastproject3:pull_request`
- **Audience:** `api://AzureADTokenExchange`

#### Credential 3: Pull Request Refs (Optional but Recommended)
- **Name:** `github-pr-refs` (or similar)
- **Issuer:** `https://token.actions.githubusercontent.com`
- **Subject:** `repo:kenderovemil/mlops-used-cars-lastproject3:ref:refs/pull/*`
- **Audience:** `api://AzureADTokenExchange`

### 3.3 Common Issues to Check
- ✓ No typos in repository name (case-sensitive)
- ✓ Owner name is correct (user or organization)
- ✓ No extra spaces in subject
- ✓ Issuer URL is exactly `https://token.actions.githubusercontent.com`
- ✓ Audience is exactly `api://AzureADTokenExchange`

**Rationale:**
- OIDC token exchange requires exact subject matching
- Wrong subject will cause "Invalid subject" errors
- Ensures all trigger types (push/PR) are covered

---

## Step 4: Validation Testing

### 4.1 Initial Test - Pull Request
1. Commit YAML changes to a feature branch
2. Push changes to GitHub
3. Create pull request targeting `main` branch
4. Observe workflow execution triggered by `pull_request` event

**Expected Results:**
- ✅ All four jobs start successfully
- ✅ Azure Login step shows "Using federated identity token"
- ✅ NO "user-assigned managed identity" messages
- ✅ Debug step shows `auth-type: 'IDENTITY'`
- ✅ All secrets present (true/true/true)

### 4.2 Secondary Test - Push to Main
1. Merge pull request to `main` branch
2. Observe workflow execution triggered by `push` event

**Expected Results:**
- ✅ Same success criteria as 4.1
- ✅ GitHub Ref shows `refs/heads/main`

### 4.3 Collect Diagnostic Logs
Save outputs to `ai_reviews/log_extracts/`:
- `azure_login_debug.txt` - Debug step outputs
- `workflow_run_summary.txt` - Run URLs and status
- `azure_login_success.txt` - Azure Login step logs

### 4.4 Checklist of Successful Events
- [ ] Login successful (no errors)
- [ ] Compute cluster created/updated
- [ ] Dataset registered
- [ ] Environment registered
- [ ] Pipeline job submitted successfully
- [ ] Pipeline job completed (if monitoring enabled)

**Rationale:**
- Validates fix works for both push and pull_request triggers
- Confirms federated credentials match actual GitHub context
- Provides evidence for troubleshooting if issues persist

---

## Step 5: Alternative Path - Python SDK Migration (If Needed)

**Use this path if azure/login@v1 continues to fail after Steps 1-4**

### 5.1 Migrate custom-create-compute.yml
**Status:** ✅ Already uses Python SDK (create_compute.py)

**Optional Enhancement:** Remove azure/login@v1 step entirely
- DefaultAzureCredential in Python SDK doesn't require azure/login@v1
- OIDC tokens are automatically available when `id-token: write` is set

### 5.2 Migrate custom-register-dataset.yml
**Replace:** Azure CLI commands with Python SDK

**Changes:**
1. Remove Azure Login step (lines 43-49)
2. Remove az ml CLI commands (lines 51-65)
3. Add Python setup and dependencies
4. Set environment variables for register_dataset.py
5. Run `python mlops/scripts/register_dataset.py`

**New workflow steps:**
```yaml
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install Python dependencies
        run: pip install azure-ai-ml azure-identity
          
      - name: Register Dataset
        env:
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          RESOURCE_GROUP: ${{ inputs.resource_group }}
          WORKSPACE_NAME: ${{ inputs.workspace_name }}
          DATASET_FILE: ${{ inputs.data_file }}
          DATASET_NAME: ${{ inputs.name }}
        run: python mlops/scripts/register_dataset.py
```

### 5.3 Migrate custom-register-environment.yml
**Replace:** Azure CLI commands with Python SDK

**Changes:**
1. Remove Azure Login step (lines 44-50)
2. Remove az ml CLI commands (lines 67-81)
3. Add Python setup and dependencies
4. Set environment variables for register_environment.py
5. Run `python mlops/scripts/register_environment.py`

**New workflow steps:**
```yaml
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install Python dependencies
        run: pip install azure-ai-ml azure-identity
          
      - name: Register Environment
        env:
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          RESOURCE_GROUP: ${{ inputs.resource_group }}
          WORKSPACE_NAME: ${{ inputs.workspace_name }}
          ENV_FILE: ${{ inputs.environment_file }}
        run: python mlops/scripts/register_environment.py
```

### 5.4 Migrate custom-run-pipeline.yml
**Replace:** Azure CLI commands with Python SDK

**Changes:**
1. Remove Azure Login step (lines 40-46)
2. Remove az ml CLI commands (lines 54-96)
3. Add Python setup and dependencies
4. Enhance run_pipeline.py with monitoring logic
5. Run `python mlops/scripts/run_pipeline.py`

**New workflow steps:**
```yaml
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install Python dependencies
        run: pip install azure-ai-ml azure-identity
          
      - name: Run Pipeline
        env:
          AZURE_SUBSCRIPTION_ID: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          RESOURCE_GROUP: ${{ inputs.resource_group }}
          WORKSPACE_NAME: ${{ inputs.workspace_name }}
          PIPELINE_FILE: ${{ inputs.parameters-file }}
          JOB_NAME: ${{ inputs.job-name }}
        run: python mlops/scripts/run_pipeline.py
```

**Note:** May need to enhance run_pipeline.py with job monitoring and validation logic currently in YAML.

**Rationale:**
- Eliminates dependency on azure/login@v1 action
- More reliable OIDC authentication through DefaultAzureCredential
- Better error messages and debugging
- Consistent with modern Azure SDK patterns
- Already proven to work in create_compute workflow

---

## Step 6: Final Cleanup

### 6.1 Remove Debug Steps (After Successful Validation)
Once workflows are stable and running without errors:
1. Remove "Debug Azure Login Context" step from all four workflows
2. Commit cleanup changes

### 6.2 Document Resolution
Create final summary documenting:
- Root cause identified
- Changes made
- Test results
- Lessons learned

### 6.3 Archive Diagnostic Evidence
Keep in `ai_reviews/log_extracts/`:
- Successful run logs
- Before/after comparisons
- Federated credential configurations

---

## Timeline and Priorities

### High Priority (Do First)
- ✅ Step 1: YAML corrections (auth-type fix)
- ✅ Step 2: Add debug steps
- ⚠️ Step 3: Verify federated credentials (manual Azure portal check)

### Medium Priority (Test and Validate)
- ⏳ Step 4: Run validation tests

### Low Priority (Only If Needed)
- ⏸️ Step 5: Python SDK migration (fallback option)
- ⏸️ Step 6: Final cleanup (after confirmed success)

---

## Success Criteria

**Workflow runs successfully when:**
1. Azure Login step completes without errors
2. No "user-assigned managed identity" messages appear
3. All four jobs complete successfully
4. Pipeline job submits and runs in Azure ML
5. Debug output shows `auth-type: 'IDENTITY'`
6. No OIDC token exchange failures

**Issue is fully resolved when:**
- Multiple successful runs on push to main
- Multiple successful runs on pull requests
- No auth-related errors for at least 5 consecutive runs
- All diagnostic evidence confirms proper OIDC authentication

---

## Rollback Plan

**If changes cause new issues:**
1. Revert YAML changes via Git
2. Return to previous working state
3. Re-analyze error messages
4. Consider Python SDK migration path (Step 5)

**If Python SDK migration fails:**
1. Keep azure/login@v1 for CLI-based workflows
2. Use Python SDK only for workflows already using it
3. Investigate azure/login@v1 version pinning
4. Consider service principal with client secret as last resort

---

## Notes

- Debug steps are temporary and should be removed after issue is resolved
- Federated credentials in Azure AD must exactly match GitHub context
- Python SDK approach is recommended long-term for better reliability
- All changes should be tested on feature branch before merging to main
- Keep diagnostic evidence in ai_reviews/ for future reference
