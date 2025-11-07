# 🤖 GitHub Copilot - MLOps Documentation Guide

## 📌 Purpose

This document defines GitHub Copilot's role specifically within the `mlops/` directory structure, complementing the main COPILOT_GUIDE.md at the root level.

## 🧠 Role within MLOps

GitHub Copilot assists with:

1. **Azure ML YAML structures** in `mlops/azureml/`
2. **Pipeline component definitions**
3. **Environment configurations**
4. **Documentation improvements** in `mlops/docs/`

## 📁 MLOps Directory Structure

```
mlops/
├── azureml/
│   └── train/
│       ├── newpipeline.yml      # Main pipeline orchestration
│       ├── prep.yml             # Data preparation component
│       ├── train.yml            # Model training component
│       ├── register.yml         # Model registration component
│       ├── train-env.yml        # Environment definition
│       ├── data.yml             # Dataset configuration
│       └── config-infra-prod.yml # Infrastructure config
├── cursor_zone/                  # ⚠️ Reserved for Cursor AI validation
├── docs/
│   ├── CURSOR_GUIDE.md          # Cursor AI documentation
│   ├── SECRETS_SETUP.md         # Azure secrets setup
│   └── COPILOT_GUIDE.md         # This file
└── test-sync/                    # Testing artifacts
```

## ✅ What Copilot Can Do

### Azure ML Pipeline Suggestions

Assist with pipeline YAML structure following Azure ML schema:

```yaml
# Example: Pipeline component structure
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline
display_name: "Used Cars Training Pipeline"

jobs:
  prep_job:
    type: command
    component: azureml:prep_component@latest
    inputs:
      raw_data:
        type: uri_file
        path: azureml:used-cars-data@latest
  
  train_job:
    type: command
    component: azureml:train_component@latest
    inputs:
      train_data: ${{parent.jobs.prep_job.outputs.train_data}}
```

### Component Definition Help

Suggest improvements to component YAMLs:

```yaml
# Example: Command component with proper metadata
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
name: data_prep
display_name: "Prepare Training Data"
version: 1.0
type: command
description: "Splits used cars dataset into train and test sets"

inputs:
  raw_data:
    type: uri_file
    description: "Input CSV file with used cars data"
  test_size:
    type: number
    default: 0.2
    description: "Proportion of data for test set"

outputs:
  train_data:
    type: uri_folder
    description: "Training dataset output"
  test_data:
    type: uri_folder
    description: "Test dataset output"

environment: azureml:train-env@latest

command: >-
  python ${{code}}/prepare.py
  --raw_data ${{inputs.raw_data}}
  --test_size ${{inputs.test_size}}

code: ../../../data-science/src
```

### Environment Configuration

Help with Conda environment specifications:

```yaml
# Example: train-conda.yml
name: train-env
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.8
  - pip=21.3
  - pandas=1.3.5
  - scikit-learn=1.0.2
  - pip:
    - azureml-core==1.47.0
    - mlflow==2.1.1
```

### Documentation Enhancement

Improve clarity and completeness of documentation files in `mlops/docs/`:

- Add examples and use cases
- Clarify technical concepts
- Improve markdown formatting
- Add troubleshooting sections

## 🚫 What Copilot Should NOT Do

1. **Do NOT modify** `CURSOR_GUIDE.md` - This is Cursor AI's domain
2. **Do NOT suggest changes** to `cursor_zone/` - Reserved for validation
3. **Do NOT expose secrets** - Always use `${{ secrets.NAME }}` in workflows
4. **Do NOT suggest** breaking changes without clear migration paths

## 🔄 Coordination with Cursor AI

GitHub Copilot and Cursor AI have complementary roles:

| Tool | Primary Focus | Directory Access |
|------|---------------|------------------|
| **GitHub Copilot** | Code completion, suggestions, documentation | All except `cursor_zone/` |
| **Cursor AI** | YAML validation, pipeline testing | `cursor_zone/`, read-only elsewhere |

**Workflow:**
1. Copilot suggests code/YAML improvements
2. Developer implements changes
3. Cursor validates YAML structure in `cursor_zone/`
4. CI/CD pipelines test the changes

## 🎯 Best Practices for MLOps Assistance

### 1. Azure ML Schema Compliance

Always ensure YAML follows Azure ML schema:

```yaml
# ✅ Good: Includes schema reference
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
type: command
name: my_component

# ❌ Bad: Missing schema reference
type: command
name: my_component
```

### 2. Input/Output Type Specifications

Be explicit about data types:

```yaml
# ✅ Good: Clear type specifications
inputs:
  dataset:
    type: uri_file
    description: "CSV file input"
  threshold:
    type: number
    default: 0.5

# ❌ Bad: Ambiguous types
inputs:
  dataset: {}
  threshold: 0.5
```

### 3. Proper Component References

Use versioned component references:

```yaml
# ✅ Good: Versioned reference
component: azureml:prep_component@latest

# ✅ Also good: Specific version
component: azureml:prep_component:1.0

# ❌ Bad: Unversioned or unclear
component: prep_component
```

### 4. Environment Consistency

Ensure environment definitions match actual code requirements:

```yaml
# ✅ Good: All required packages listed
dependencies:
  - python=3.8
  - pandas=1.3.5
  - scikit-learn=1.0.2
  - pip:
    - azureml-core==1.47.0

# ❌ Bad: Missing dependencies that code uses
dependencies:
  - python=3.8
  - pandas
```

## 📋 Common Tasks

### Adding a New Pipeline Component

When suggesting a new component:

1. Create component YAML in `azureml/train/`
2. Define clear inputs/outputs
3. Reference the Python script location
4. Specify environment dependencies
5. Add to pipeline orchestration in `newpipeline.yml`

### Updating Pipeline Logic

When modifying pipelines:

1. Review existing job definitions
2. Ensure data flow between jobs is correct
3. Update component versions if needed
4. Test changes in `cursor_zone/` first

### Enhancing Documentation

When improving docs:

1. Check for outdated information
2. Add missing examples
3. Clarify complex concepts
4. Update version numbers and dates

## 🔍 Validation Process

After Copilot suggestions are implemented:

1. **Developer review** - Human approval of changes
2. **Cursor validation** - YAML structure validation in `cursor_zone/`
3. **CI/CD testing** - GitHub Actions run workflows
4. **Azure ML execution** - Actual pipeline run in Azure

## 📚 Reference Materials

Essential reading for MLOps assistance:

- [Azure ML CLI v2 Documentation](https://learn.microsoft.com/en-us/azure/machine-learning/how-to-train-cli)
- [Azure ML Pipeline YAML Schema](https://azuremlschemas.azureedge.net/)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- Project-specific: `SECRETS_SETUP.md`, main `README.md`

## 🎓 Learning from the Project

Key patterns to follow in this project:

1. **Error handling**: Scripts use try-except with detailed error messages
2. **Logging**: Liberal use of `print(..., flush=True)` for debugging
3. **Diagnostics**: JSON diagnostic files track execution status
4. **Validation**: Multi-stage validation (local → cursor → CI/CD → Azure)

## 💬 Communication Style

When providing suggestions:

- **Be specific**: Reference exact files and line numbers
- **Explain why**: Help developers understand the reasoning
- **Offer alternatives**: Provide multiple approaches when applicable
- **Respect context**: Consider the existing codebase patterns

## 🎉 Welcome!

Thank you for assisting with this MLOps project. Your suggestions help create robust, maintainable machine learning pipelines!

---

*See also: Root-level `COPILOT_GUIDE.md` for general guidelines*  
*Last updated: 2025-11-07*
