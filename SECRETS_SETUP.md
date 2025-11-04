# Azure Secrets Setup for GitHub Actions

This document explains how to configure Azure credentials as GitHub secrets for the MLOps pipeline workflows.

## Required GitHub Secrets

The workflows in this repository require the following four individual secrets to authenticate with Azure:

1. **AZURE_CLIENT_ID** - The Application (client) ID of your Azure Service Principal
2. **AZURE_CLIENT_SECRET** - The client secret (password) of your Azure Service Principal
3. **AZURE_TENANT_ID** - The Directory (tenant) ID of your Azure Active Directory
4. **AZURE_SUBSCRIPTION_ID** - The ID of your Azure subscription

## How to Create Azure Service Principal

If you don't have an Azure Service Principal yet, follow these steps:

1. **Login to Azure CLI:**
   ```bash
   az login
   ```

2. **Create a Service Principal:**
   ```bash
   az ad sp create-for-rbac --name "mlops-used-cars-sp" --role contributor \
       --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group-name} \
       --sdk-auth
   ```
   
   Replace `{subscription-id}` and `{resource-group-name}` with your actual values.

3. **Save the output** - The command will return JSON containing your credentials:
   ```json
   {
     "clientId": "YOUR_CLIENT_ID",
     "clientSecret": "YOUR_CLIENT_SECRET",
     "subscriptionId": "YOUR_SUBSCRIPTION_ID",
     "tenantId": "YOUR_TENANT_ID",
     ...
   }
   ```

## How to Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click on **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each of the four secrets:
   - Name: `AZURE_CLIENT_ID`, Value: [your client ID]
   - Name: `AZURE_CLIENT_SECRET`, Value: [your client secret]
   - Name: `AZURE_TENANT_ID`, Value: [your tenant ID]
   - Name: `AZURE_SUBSCRIPTION_ID`, Value: [your subscription ID]

## Workflows That Use These Secrets

The following workflows require these secrets:

- `deploy-model-training-pipeline-classical.yml` - Main MLOps pipeline
  - Calls `custom-create-compute.yml` - Creates Azure ML compute cluster
  - Calls `custom-register-dataset.yml` - Registers datasets in Azure ML
  - Calls `custom-register-environment.yml` - Registers ML environments
  - Calls `custom-run-pipeline.yml` - Runs the ML training pipeline

## Troubleshooting

### AuthenticationFailed Error

If you see an error like:
```
ERROR: Operation returned an invalid status 'Server failed to authenticate the request. 
Make sure the value of Authorization header is formed correctly including the signature.'
ErrorCode:AuthenticationFailed
```

This means the Azure credentials are not properly configured. Check that:

1. All four secrets (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, AZURE_SUBSCRIPTION_ID) are set in GitHub
2. The Service Principal has the necessary permissions on the resource group
3. The secrets contain the correct values (no extra spaces or quotes)

### Service Principal Permissions

The Service Principal needs at least **Contributor** role on the resource group containing your Azure Machine Learning workspace.

To verify or assign permissions:

```bash
az role assignment list --assignee YOUR_CLIENT_ID --scope /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP
```

To add Contributor role if missing:

```bash
az role assignment create --assignee YOUR_CLIENT_ID \
    --role Contributor \
    --scope /subscriptions/YOUR_SUBSCRIPTION_ID/resourceGroups/YOUR_RESOURCE_GROUP
```

## Security Best Practices

1. **Never commit secrets** to your repository
2. **Rotate secrets regularly** (every 90 days recommended)
3. **Use least privilege** - only grant the minimum required permissions
4. **Monitor service principal usage** in Azure Portal
5. **Use separate service principals** for different environments (dev, staging, prod)
