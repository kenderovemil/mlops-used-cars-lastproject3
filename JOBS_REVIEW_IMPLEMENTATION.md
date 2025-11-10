# Azure ML Jobs Review - Implementation Summary

## Overview

This implementation provides a Python script that queries the Azure ML workspace and generates a review of the last 5 jobs.

## Problem Statement Addressed

The script fulfills the following requirements:
1. ✅ Calls the Azure ML SDK (`azure.ai.ml`)
2. ✅ Reviews the last 5 jobs from the `project_III_MLOPS` workspace
3. ✅ For each job, outputs:
   - Job ID
   - Display name
   - Status (Completed, Failed, Running)
   - Dataset input (if available)
   - Start time and End time
4. ✅ Saves the results in a markdown table in the `ai_reviews/` folder as `jobs_review.md`

## Files Added

### 1. `ai_reviews/review_jobs.py`
The main Python script that:
- Connects to the Azure ML workspace using `azure.ai.ml.MLClient`
- Retrieves the last 5 jobs using `ml_client.jobs.list(max_results=5)`
- Extracts job information including:
  - Job ID (job.name)
  - Display Name (job.display_name)
  - Status (job.status)
  - Dataset input (extracted from job.inputs)
  - Start Time (job.creation_context.created_at)
  - End Time (job.creation_context.last_modified_at or job.properties.end_time)
- Formats the data into a markdown table
- Saves to `ai_reviews/jobs_review.md`

### 2. `ai_reviews/requirements.txt`
Lists the required dependencies:
- `azure-ai-ml>=1.11.0`
- `azure-identity>=1.15.0`

### 3. `ai_reviews/JOBS_REVIEW_README.md`
Comprehensive documentation covering:
- Prerequisites
- Installation instructions
- Usage (both manual and using the convenience script)
- Output format
- Troubleshooting guide

### 4. `ai_reviews/run_review.sh`
A convenience bash script that:
- Installs dependencies from requirements.txt
- Executes the review_jobs.py script
- Makes it easy to run the review with a single command

### 5. `ai_reviews/jobs_review_sample.md`
An example output file showing the expected table format with sample data.

## Usage

### Prerequisites
Set the following environment variables:
```bash
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export RESOURCE_GROUP="your-resource-group"
```

You also need to be authenticated to Azure (e.g., via `az login`).

### Quick Start
```bash
cd ai_reviews
./run_review.sh
```

### Manual Execution
```bash
cd ai_reviews
pip install -r requirements.txt
python review_jobs.py
```

### Output
The script generates `ai_reviews/jobs_review.md` with a table in this format:

```markdown
# Azure ML Jobs Review

**Workspace:** project_III_MLOPS
**Generated:** 2025-11-10 19:48:00

| Job ID | Display Name | Status | Dataset | Start Time | End Time |
|--------|--------------|--------|---------|------------|----------|
| job_123 | prep-data-job | Completed | azureml:used-cars-raw:1 | 2025-11-08 14:30:00 | 2025-11-08 14:35:00 |
...
```

## Implementation Details

### Error Handling
The script includes robust error handling for:
- Missing environment variables
- Connection failures to Azure ML workspace
- Empty job lists
- Missing job attributes

### Compatibility
- Works with the existing repository structure
- Uses the same authentication approach as other scripts in `mlops/scripts/`
- Imports the `load_credentials` utility if available
- Falls back to environment variables if credentials file is not accessible

### Dataset Extraction
The script intelligently extracts dataset information from job inputs:
- Checks for `path` attribute in input values
- Falls back to string representation if path is not available
- Returns "N/A" if no dataset input is found

### Time Formatting
- Handles both datetime objects and string timestamps
- Uses consistent format: `YYYY-MM-DD HH:MM:SS`
- Shows "N/A" for jobs that don't have end times (e.g., Running jobs)

## Testing Notes

⚠️ **Important**: This script requires valid Azure credentials and access to the `project_III_MLOPS` workspace. Testing requires:

1. Valid Azure subscription
2. Access to the resource group
3. Permissions to read jobs from the workspace
4. At least one job in the workspace

To test locally:
```bash
# Set environment variables
export AZURE_SUBSCRIPTION_ID="your-sub-id"
export RESOURCE_GROUP="your-rg"

# Login to Azure
az login

# Run the script
cd ai_reviews
python review_jobs.py
```

## Future Enhancements

Possible improvements for future iterations:
- Add filtering by job status or date range
- Export to CSV or DOCX format in addition to markdown
- Add job duration calculation
- Include error messages from failed jobs
- Add pagination support for more than 5 jobs
- Create automated tests with mocked Azure ML client

## Security Considerations

- The script uses `DefaultAzureCredential` which follows the Azure SDK authentication best practices
- No credentials are hardcoded in the script
- Environment variables are the primary method for configuration
- The script does not expose or log sensitive information

## Maintenance

To update the script:
1. Modify `ai_reviews/review_jobs.py`
2. Update documentation in `ai_reviews/JOBS_REVIEW_README.md`
3. Test changes locally with valid Azure credentials
4. Update the sample output in `jobs_review_sample.md` if the format changes
