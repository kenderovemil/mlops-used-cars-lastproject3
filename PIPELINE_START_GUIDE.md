# MLOps Pipeline Start Guide

## Overview
This guide explains how the MLOps pipeline for used car pricing has been started and how it works.

## Pipeline Architecture

### Main Pipeline Components
The pipeline is defined in `mlops/azureml/train/newpipeline.yml` and consists of four stages:

1. **Data Preparation** (`prep_data`)
   - Component: `azureml:prep_data_component:1`
   - Input: Raw CSV data from `data/used_cars_raw.csv`
   - Output: Cleaned data ready for training
   - Compute: `cpu-cluster`

2. **Model Training** (`train_model`)
   - Component: `azureml:train_model_component:1`
   - Input: Cleaned data from prep_data stage
   - Output: Trained model
   - Compute: `cpu-cluster`

3. **Model Tuning** (`tune_model`)
   - Component: `azureml:tune_model_component:1`
   - Input: Model from training stage
   - Output: Optimized best model
   - Compute: `cpu-cluster`

4. **Model Registration** (`register_model`)
   - Component: `azureml:register_model_component:1`
   - Input: Best model from tuning stage
   - Output: Registered model in Azure ML
   - Compute: `cpu-cluster`

## GitHub Actions Workflows

### Primary Pipeline Workflow: `azureml-pipeline.yml`
**Location**: `.github/workflows/azureml-pipeline.yml`

**Triggers**:
- Manual trigger via `workflow_dispatch`
- Automatic trigger on push to:
  - `mlops/azureml/train/newpipeline.yml`
  - `.github/workflows/azureml-pipeline.yml`

**What it does**:
1. Checks out the repository
2. Logs into Azure
3. Sets up Python and Azure ML SDK
4. Copies data files to the correct location
5. Validates Azure resources (resource group, workspace)
6. Submits the ML pipeline job to Azure ML
7. Monitors the job until completion

### Full Deployment Pipeline: `deploy-model-training-pipeline-classical.yml`
**Location**: `.github/workflows/deploy-model-training-pipeline-classical.yml`

**Triggers**:
- Push to `main` branch
- Pull requests to `main` branch

**What it does**:
1. Creates compute cluster
2. Registers dataset
3. Registers environment
4. Runs the full pipeline

## How the Pipeline Was Started

### Action Taken
A documentation comment was added to `mlops/azureml/train/newpipeline.yml`:
```yaml
# Pipeline activated - Ready to process used car pricing data
```

### Why This Works
1. The `.github/workflows/azureml-pipeline.yml` workflow monitors changes to `newpipeline.yml`
2. When the file is modified and pushed, the workflow automatically triggers
3. The workflow submits the pipeline to Azure ML for execution

### Current Status
✅ Pipeline has been activated by committing a change to `mlops/azureml/train/newpipeline.yml`
✅ GitHub Actions workflow should be triggered automatically
✅ The workflow will submit the job to Azure ML workspace: `project_III_MLOPS`
✅ Resource group: `streaming_autovehicle_pricing_MLOPS`

## Monitoring the Pipeline

### Check GitHub Actions
1. Go to: https://github.com/kenderovemil/mlops-used-cars-lastproject3/actions
2. Look for the "Run AzureML Pipeline" workflow
3. Click on the latest run to see detailed logs

### Check Azure ML Studio
1. Log into Azure Portal
2. Navigate to Azure ML workspace: `project_III_MLOPS`
3. Go to "Jobs" section
4. Find the pipeline run (named `full_pipeline`)

## Manual Pipeline Trigger

If you need to manually trigger the pipeline without code changes:

### Option 1: GitHub Actions UI
1. Go to: https://github.com/kenderovemil/mlops-used-cars-lastproject3/actions
2. Select "Run AzureML Pipeline" workflow
3. Click "Run workflow" button
4. Select branch and click "Run workflow"

### Option 2: Azure ML SDK
```bash
az ml job create \
  --file mlops/azureml/train/newpipeline.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS
```

## Required Secrets

The pipeline requires these GitHub secrets to be configured:
- `AZURE_CREDENTIALS`: Azure service principal credentials
- `AZURE_STORAGE_KEY`: Azure Storage account key

## Expected Outcomes

When the pipeline completes successfully, you will have:
1. ✅ Cleaned and preprocessed used car data
2. ✅ Trained Random Forest Regressor model
3. ✅ Optimized model with best hyperparameters
4. ✅ Registered model in Azure ML Model Registry
5. ✅ MLflow metrics and artifacts logged

## Business Impact

This automated pipeline provides:
- **Improved Accuracy**: Data-driven pricing decisions
- **Scalability**: Automated retraining and updates
- **Efficiency**: No manual intervention required
- **Consistency**: Standardized preprocessing and training
- **Traceability**: Full MLflow tracking of experiments

## Troubleshooting

### Pipeline Not Triggering
- Verify the file path in the trigger matches: `mlops/azureml/train/newpipeline.yml`
- Check GitHub Actions permissions
- Verify secrets are configured

### Azure Authentication Issues
- Verify `AZURE_CREDENTIALS` secret is valid
- Check service principal has necessary permissions
- Ensure workspace and resource group exist

### Job Failures
- Check Azure ML Studio for detailed error logs
- Verify compute cluster `cpu-cluster` exists
- Ensure all components are registered in Azure ML
- Verify data file exists at `data/used_cars_raw.csv`

## Next Steps

1. Monitor the current pipeline run
2. Review model metrics in MLflow
3. Validate model performance
4. Deploy the registered model (if satisfactory)
5. Set up monitoring and retraining schedules
