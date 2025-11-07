# Azure Login Coverage Verification

This document verifies that all GitHub workflows in this repository support full Azure login coverage across all contexts using Federated Identity (OIDC).

## Verification Date
Last verified: 2025-11-07

## Workflows Using Azure Login

The following workflows use `azure/login@v1` with OIDC (Federated Identity):

1. **custom-create-compute.yml** - Creates Azure ML compute clusters
2. **custom-register-dataset.yml** - Registers datasets in Azure ML
3. **custom-register-environment.yml** - Registers ML environments
4. **custom-run-pipeline.yml** - Runs ML training pipelines

## Verification Results

### ✅ No Conditional Login Constraints
All Azure Login steps are executed unconditionally. There are no `if:` conditions such as:
- ❌ `if: github.ref == 'refs/heads/main'` (NOT FOUND - Good!)
- ❌ `if: github.event_name == 'push'` (NOT FOUND - Good!)
- ❌ Any other branch or context restrictions (NOT FOUND - Good!)

### ✅ OIDC Configuration
All workflows properly use OpenID Connect (Federated Identity):
- All have `id-token: write` permission
- All use `client-id`, `tenant-id`, and `subscription-id` parameters
- No client secrets required (more secure than traditional authentication)

### ✅ Broad Context Support
- **Reusable Workflows**: All custom workflows use `workflow_call` trigger, which allows them to be called from any context (push, pull_request, workflow_dispatch, etc.)
- **Main Workflow**: `deploy-model-training-pipeline-classical.yml` runs on both `push` to main and `pull_request` to main
- **Result**: Azure login will work in all supported GitHub contexts

## Architecture

```
deploy-model-training-pipeline-classical.yml (runs on: push, pull_request)
├── custom-create-compute.yml (workflow_call with Azure login)
├── custom-register-dataset.yml (workflow_call with Azure login)
├── custom-register-environment.yml (workflow_call with Azure login)
└── custom-run-pipeline.yml (workflow_call with Azure login)
```

Each reusable workflow:
1. Has `permissions: { id-token: write, contents: read }`
2. Performs Azure login using OIDC
3. Can be called from any context without restrictions

## Federated Identity Subject Claims

With the current configuration, Azure Federated Identity supports these subject claims:

- `repo:<org>/<repo>:ref:refs/heads/main` - Push to main branch
- `repo:<org>/<repo>:pull_request` - Pull requests
- `repo:<org>/<repo>:environment:<name>` - Environment-specific deployments
- Any other GitHub OIDC subject claims as configured in Azure

The workflows do not restrict which subject claims can be used, providing maximum flexibility.

## Compliance Statement

✅ **All workflows comply with the requirement for full Azure login coverage across all GitHub workflow contexts using Federated Identity (OIDC).**

No conditional constraints were found that would limit Azure login to specific branches, events, or contexts.
