# Azure ML Jobs Review Script

This script retrieves and reviews the last 5 jobs from the Azure ML workspace `project_III_MLOPS`.

## Prerequisites

1. **Azure CLI or Azure credentials**: You need to be authenticated to Azure
2. **Python packages**: `azure-ai-ml`, `azure-identity`
3. **Environment variables**:
   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID
   - `RESOURCE_GROUP`: The resource group containing the workspace

## Installation

Install required Python packages:

```bash
pip install -r requirements.txt
```

Or install packages individually:

```bash
pip install azure-ai-ml azure-identity pandas reportlab
```

## Usage

### Option 1: Using the convenience script

```bash
cd ai_reviews
./run_review.sh
```

The script will:
1. Install required dependencies
2. Run the review script
3. Generate three output files:
   - `jobs_review.md` (Markdown table)
   - `job_review.csv` (CSV format)
   - `job_review.pdf` (PDF report)

### Option 2: Manual execution

#### Set Environment Variables

```bash
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export RESOURCE_GROUP="your-resource-group"
```

#### Run the Script

```bash
cd ai_reviews
python review_jobs.py
```

### Output

The script will generate three files in the `ai_reviews/` directory:

1. **jobs_review.md** - Markdown table format
2. **job_review.csv** - CSV format for data analysis
3. **job_review.pdf** - Professional PDF report

Each file contains the following information for the last 5 jobs:

- Job ID
- Display Name
- Status (Completed, Failed, Running, etc.)
- Dataset Input (if available)
- Start Time
- End Time

## Example Output Format

```markdown
# Azure ML Jobs Review

**Workspace:** project_III_MLOPS
**Generated:** 2025-11-10 19:48:00

| Job ID | Display Name | Status | Dataset | Start Time | End Time |
|--------|--------------|--------|---------|------------|----------|
| job_123 | train-model | Completed | azureml:used-cars-train:1 | 2025-11-10 10:00:00 | 2025-11-10 10:15:00 |
```

## Troubleshooting

### Authentication Errors

If you encounter authentication errors:

1. Make sure you're logged in to Azure CLI:
   ```bash
   az login
   ```

2. Verify your subscription and resource group:
   ```bash
   az account show
   az group list
   ```

### Missing Jobs

If no jobs are returned, verify:
- The workspace name is correct (`project_III_MLOPS`)
- You have access to the workspace
- There are jobs in the workspace (check Azure ML Studio)
