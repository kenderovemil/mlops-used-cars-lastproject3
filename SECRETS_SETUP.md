# Azure Secrets Setup for GitHub Actions

This document explains how to configure Azure credentials as GitHub secrets for the MLOps pipeline workflows using OIDC (OpenID Connect) authentication with Workload Identity Federation.

## Authentication Method: OIDC (Workload Identity Federation)

This repository uses OIDC authentication which is more secure than traditional service principal secrets because:
- No secrets are stored in GitHub (passwordless authentication)
- Uses short-lived tokens that are automatically rotated
- Provides better audit trails and security

## Required GitHub Secrets

The workflows in this repository require the following three secrets to authenticate with Azure using OIDC:

1. **AZURE_CLIENT_ID** - The Application (client) ID of your Azure App Registration
2. **AZURE_TENANT_ID** - The Directory (tenant) ID of your Azure Active Directory
3. **AZURE_SUBSCRIPTION_ID** - The ID of your Azure subscription

**Note:** Unlike the old method, you do NOT need AZURE_CLIENT_SECRET with OIDC authentication.

## Setup Instructions

### 1. App Registration Setup in Azure

1. **Go to Azure Portal** → **Microsoft Entra ID** → **App registrations**
2. **Create or select an App Registration** for your MLOps pipeline
3. **Note down the Application (client) ID** - this will be your `AZURE_CLIENT_ID`
4. **In the left menu**, go to **Certificates & secrets** → **Federated credentials**
5. **Click "Add credential"** and configure:
   - **Federated credential scenario**: GitHub Actions deploying Azure resources
   - **Organization**: Your GitHub username or organization (e.g., `kenderovemil`)
   - **Repository**: Your repository name (e.g., `mlops-used-cars-lastproject3`)
   - **Entity type**: Branch
   - **GitHub branch name**: The branch you want to authenticate from (e.g., `main`)
   - **Name**: A descriptive name (e.g., `github-actions-main-branch`)
   
   This will create a subject identifier like:
   ```
   repo:kenderovemil/mlops-used-cars-lastproject3:ref:refs/heads/main
   ```

6. **Note**: The audience will automatically be set to `api://AzureADTokenExchange` and issuer to `https://token.actions.githubusercontent.com`

### 2. Assign Azure Permissions

The App Registration needs appropriate permissions to manage Azure ML resources:

```bash
# Login to Azure
az login

# Assign Contributor role to the App Registration
az role assignment create \
  --assignee YOUR_CLIENT_ID \
  --role Contributor \
  --scope /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP
```

### 3. Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each of the three secrets:
   - Name: `AZURE_CLIENT_ID`, Value: [your application/client ID]
   - Name: `AZURE_TENANT_ID`, Value: [your tenant ID]
   - Name: `AZURE_SUBSCRIPTION_ID`, Value: [your subscription ID]

### 4. Workflow Configuration

The workflows are already configured to use OIDC authentication with the following structure:

```yaml
permissions:
  id-token: write
  contents: read

jobs:
  your-job:
    runs-on: ubuntu-latest
    steps:
      - name: Azure Login
        uses: azure/login@v1
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          auth-type: IDENTITY
```

**Important:** The `auth-type` must be set to `IDENTITY` (not `OIDC` or `MANAGED_IDENTITY`).

## Workflows That Use OIDC Authentication

The following workflows use OIDC authentication:

- `deploy-model-training-pipeline-classical.yml` - Main MLOps pipeline
  - Calls `custom-create-compute.yml` - Creates Azure ML compute cluster
  - Calls `custom-register-dataset.yml` - Registers datasets in Azure ML
  - Calls `custom-register-environment.yml` - Registers ML environments
  - Calls `custom-run-pipeline.yml` - Runs the ML training pipeline
- `azureml-pipeline.yml` - Alternative pipeline workflow

## Troubleshooting

### AuthenticationFailed Error

If you see an error like:
```
ERROR: AADSTS70021: No matching federated identity record found for presented assertion.
```

This means the federated credential is not properly configured. Check that:

1. The federated credential subject matches your repository and branch exactly
2. The workflow is running from the branch specified in the federated credential
3. All three secrets (AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID) are set in GitHub
4. The App Registration has the necessary permissions on the resource group

### Permissions Error

If you see:
```
ERROR: The client does not have authorization to perform action
```

Verify that:
1. The App Registration has Contributor role (or appropriate role) on the resource group
2. The role assignment scope includes the resources you're trying to access

To check role assignments:
```bash
az role assignment list --assignee YOUR_CLIENT_ID
```

### Token Errors

If you see token-related errors:
1. Ensure your workflow has `permissions: id-token: write` at the workflow level
2. Verify the `auth-type: IDENTITY` is set in the Azure login step
3. Check that the azure/login action version is v1 or later

## Security Best Practices

1. **Use branch protection** - Only allow workflows to run from protected branches
2. **Limit federated credentials** - Create separate credentials for each branch/environment
3. **Use least privilege** - Only grant the minimum required permissions to the App Registration
4. **Monitor usage** - Review Azure Activity Logs to monitor App Registration usage
5. **Use separate App Registrations** - Create different App Registrations for different environments (dev, staging, prod)
6. **Audit federated credentials** - Regularly review and remove unused federated credentials

## Migration from Service Principal Secrets

If you were previously using the old method with `AZURE_CREDENTIALS` secret:

1. Follow the setup instructions above to configure OIDC
2. Update your workflows to use the new authentication method
3. **After confirming OIDC works**, you can safely remove the `AZURE_CREDENTIALS` and `AZURE_CLIENT_SECRET` secrets
4. Consider rotating or deleting the old client secret in Azure if it's no longer needed

## Additional Resources

- [Azure Login Action Documentation](https://github.com/Azure/login)
- [GitHub Actions OIDC with Azure](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-azure)
- [Azure Workload Identity Federation](https://learn.microsoft.com/en-us/azure/active-directory/workload-identities/workload-identity-federation)
