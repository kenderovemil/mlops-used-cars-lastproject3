# YAML Input Reference Review

## Overview
This report identifies incorrect input references in Azure ML pipeline YAML files. When a job is part of a pipeline (type: pipeline), it should reference pipeline inputs using `parent.inputs.*` instead of `inputs.*`.

## Summary
- **Total files reviewed**: 24
- **Pipeline files found**: 2
- **Issues found**: 2

## Issues Identified

| File | Line | Incorrect expression | Suggested correction |
|------|------|----------------------|----------------------|
| github_workflows/newpipeline.yml | 12 | `${{inputs.training_data}}` | `${{parent.inputs.training_data}}` |
| mlops/azureml/train/newpipeline.yml | 12 | `${{inputs.training_data}}` | `${{parent.inputs.training_data}}` |

## Details

### 1. github_workflows/newpipeline.yml
- **Line 12**: Inside the `prep_data` job within a pipeline
- **Current**: `raw_data: ${{inputs.training_data}}`
- **Should be**: `raw_data: ${{parent.inputs.training_data}}`
- **Reason**: The job is part of a pipeline and needs to reference the parent pipeline's inputs

### 2. mlops/azureml/train/newpipeline.yml
- **Line 12**: Inside the `prep_data` job within a pipeline
- **Current**: `raw_data: ${{inputs.training_data}}`
- **Should be**: `raw_data: ${{parent.inputs.training_data}}`
- **Reason**: The job is part of a pipeline and needs to reference the parent pipeline's inputs

## Explanation

In Azure ML pipelines:
- **Pipeline-level inputs** are defined at the top level under `inputs:`
- **Jobs within pipelines** reference these inputs using `${{parent.inputs.*}}`
- **Standalone components/jobs** use `${{inputs.*}}` to reference their own inputs

The incorrect usage of `${{inputs.*}}` instead of `${{parent.inputs.*}}` within pipeline jobs can cause runtime errors because the job will look for inputs in its own scope rather than the parent pipeline's scope.

## Automatic Corrections

The following automatic corrections have been applied to fix these issues:

1. **github_workflows/newpipeline.yml** - Line 12: Changed `${{inputs.training_data}}` to `${{parent.inputs.training_data}}`
2. **mlops/azureml/train/newpipeline.yml** - Line 12: Changed `${{inputs.training_data}}` to `${{parent.inputs.training_data}}`

## Verification

After applying the corrections:
- Both pipeline files now correctly reference parent inputs
- Pipeline jobs can properly access the pipeline-level input parameters
- No other YAML files in the repository have this issue

---
*Report generated on: 2025-11-10*
