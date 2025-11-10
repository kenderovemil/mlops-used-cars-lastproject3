# Quick Start Guide: Azure ML Jobs Review

This guide helps you run the Azure ML jobs review script.

## Step 1: Prerequisites

Ensure you have:
- Python 3.7 or higher
- Access to Azure ML workspace `project_III_MLOPS`
- Azure CLI installed (optional but recommended)

## Step 2: Authentication

### Option A: Azure CLI Login
```bash
az login
```

### Option B: Set Environment Variables
```bash
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export RESOURCE_GROUP="your-resource-group"
```

To find these values:
```bash
# List subscriptions
az account list --output table

# List resource groups
az group list --output table
```

## Step 3: Run the Script

### Simple Method (Recommended)
```bash
cd ai_reviews
./run_review.sh
```

### Manual Method
```bash
cd ai_reviews
pip install -r requirements.txt
python review_jobs.py
```

## Step 4: View Results

The script will generate `ai_reviews/jobs_review.md` with a table like this:

```markdown
# Azure ML Jobs Review

**Workspace:** project_III_MLOPS
**Generated:** 2025-11-10 19:48:00

| Job ID | Display Name | Status | Dataset | Start Time | End Time |
|--------|--------------|--------|---------|------------|----------|
| eager_coconut_abc123 | prep-data-job | Completed | azureml:used-cars-raw:1 | 2025-11-08 14:30:00 | 2025-11-08 14:35:00 |
...
```

You can view this file in any text editor or markdown viewer.

## Troubleshooting

### "Could not initialize ML Client"
- Verify you're logged in: `az login`
- Check environment variables are set correctly
- Verify you have access to the workspace

### "No jobs found in the workspace"
- Verify the workspace name is correct
- Check that jobs exist in Azure ML Studio
- Ensure you have permissions to view jobs

### Import errors
- Run: `pip install -r requirements.txt`
- Verify Python version: `python --version` (should be 3.7+)

## Example Output

After successful execution, you'll see:

```
✅ Connected to workspace: project_III_MLOPS
📋 Retrieving jobs from workspace: project_III_MLOPS
✅ Found 5 jobs

✅ Jobs review saved to: /path/to/ai_reviews/jobs_review.md

Preview of the table:
# Azure ML Jobs Review
...
```

## Next Steps

- Open `jobs_review.md` to view the full report
- Share the markdown file with your team
- Run the script regularly to track job history
- Integrate into CI/CD pipelines if needed

## Need Help?

Refer to:
- `JOBS_REVIEW_README.md` - Detailed documentation
- `JOBS_REVIEW_IMPLEMENTATION.md` - Technical details
- `jobs_review_sample.md` - Example output
