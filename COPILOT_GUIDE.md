# 🤖 GitHub Copilot Guide

## 📌 Welcome!

Welcome, GitHub Copilot! You are invited to assist with this MLOps project for used car price prediction. This document outlines your role, the areas where you can help, and the boundaries to respect.

## 🎯 Your Role

As GitHub Copilot, you are a valued assistant whose mission is to:

- **Suggest YAML structures** for Azure ML pipelines, components, and GitHub Actions workflows
- **Provide Python code completion** for data preparation, model training, and MLOps scripts
- **Refine documentation** to improve clarity, completeness, and maintainability

## 📁 Areas of Assistance

### 1. YAML Structure Suggestions

You can assist with YAML files in the following areas:

| Directory | Purpose | Examples |
|-----------|---------|----------|
| `mlops/azureml/train/` | Azure ML pipeline definitions | `newpipeline.yml`, `prep.yml`, `train.yml`, `register.yml` |
| `.github/workflows/` | GitHub Actions CI/CD workflows | `deploy-model-training-pipeline-classical.yml` |
| `data-science/components/` | Azure ML component definitions | `prep_component.yml` |
| `data-science/environment/` | Conda environment specifications | `train_conda.yml` |

**Guidelines for YAML assistance:**
- Follow Azure ML YAML schema conventions
- Use consistent indentation (2 spaces)
- Include descriptive comments for complex configurations
- Validate references to secrets using `${{ secrets.NAME }}` syntax
- Ensure proper Azure ML component versioning

### 2. Python Code Completion

You can provide code suggestions for Python files in:

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `data-science/src/` | ML pipeline scripts | `prepare.py`, `train.py`, `register.py` |
| `src/` | Additional utility scripts | `train.py` |
| `mlops/cursor_zone/` | Validation scripts | `cursor_check.py` |

**Guidelines for Python assistance:**
- Follow existing code style and patterns
- Include type hints where appropriate
- Add docstrings for functions and classes
- Handle errors gracefully with try-except blocks
- Use logging and debug prints for troubleshooting
- Follow pandas and scikit-learn best practices

**Code Style Examples:**

```python
# Good: Clear function with docstring and error handling
def parse_args():
    """Parse command line arguments for data preparation."""
    parser = argparse.ArgumentParser(description="Prepare dataset for training")
    parser.add_argument("--raw_data", required=True, help="Path to raw data file")
    return parser.parse_args()

# Good: Defensive programming with helpful error messages
if not os.path.exists(raw_path):
    print(f"[ERROR] Raw data path does not exist: {raw_path}", flush=True)
    sys.exit(1)
```

### 3. Documentation Refinement

You can help improve documentation in:

| File | Purpose |
|------|---------|
| `README.md` | Main project overview |
| `SECRETS_SETUP.md` | Azure secrets configuration guide |
| `mlops/docs/CURSOR_GUIDE.md` | Cursor AI role definition |
| Component/script docstrings | Inline documentation |

**Guidelines for documentation:**
- Use clear, concise language
- Include practical examples
- Keep formatting consistent with existing style
- Add emoji for visual clarity (✅, ⚠️, 📌, etc.)
- Structure with proper markdown headers
- Include troubleshooting sections where relevant

## 🔐 Secrets and Security

**IMPORTANT:** Always respect the security guidelines defined in `SECRETS_SETUP.md`:

- **NEVER** reveal or hardcode secrets in code
- Use `${{ secrets.NAME }}` syntax in GitHub Actions
- Reference these GitHub Secrets:
  - `AZURE_CLIENT_ID` - Azure Service Principal client ID
  - `AZURE_CLIENT_SECRET` - Azure Service Principal secret
  - `AZURE_TENANT_ID` - Azure tenant ID
  - `AZURE_SUBSCRIPTION_ID` - Azure subscription ID
  - `GH_TOKEN` - GitHub personal access token (optional)
  - `MLFLOW_TRACKING_URI` - MLflow server URI (optional)
  - `MLFLOW_API_TOKEN` - MLflow API token (optional)

## 🚫 Boundaries and Restrictions

Please respect these boundaries:

1. **Do NOT modify** the following unless explicitly invited:
   - `mlops/docs/CURSOR_GUIDE.md` - Reserved for Cursor AI
   - `mlops/cursor_zone/` - Reserved for validation tasks
   - `.github/agents/` - Agent configuration files

2. **Do NOT suggest**:
   - Hardcoded credentials or secrets
   - Breaking changes to existing working pipelines
   - Removal of error handling or logging
   - Changes that bypass Azure ML security

3. **Always ensure**:
   - Suggestions align with Azure ML best practices
   - Code maintains backward compatibility
   - YAML syntax is valid and testable
   - Documentation remains accurate

## 🧘 Best Practices

### When Suggesting YAML

```yaml
# Good: Well-structured Azure ML component
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
name: prep_data
display_name: "Data Preparation"
version: 1
type: command

inputs:
  raw_data:
    type: uri_file
    description: "Raw CSV file for used cars"
  test_size:
    type: number
    default: 0.2

outputs:
  train_data:
    type: uri_folder
  test_data:
    type: uri_folder

command: >-
  python prepare.py
  --raw_data ${{inputs.raw_data}}
  --test_size ${{inputs.test_size}}
```

### When Completing Python Code

```python
# Good: Defensive, logged, and maintainable
def load_and_validate_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV file and perform basic validation.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Validated pandas DataFrame
        
    Raises:
        ValueError: If file doesn't exist or contains no data
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    df = pd.read_csv(file_path)
    print(f"[INFO] Loaded {len(df)} rows from {file_path}", flush=True)
    
    if df.empty:
        raise ValueError("Dataset is empty")
    
    return df
```

### When Refining Documentation

```markdown
## Good Documentation Structure

### Clear Section Headers
Use descriptive headers that guide the reader.

### Code Examples
Always include practical examples:
```bash
# Example command
python prepare.py --raw_data data/used_cars.csv
```

### Troubleshooting
Anticipate common issues and provide solutions.
```

## 📚 Reference Documents

Before making suggestions, please review:

- **CURSOR_GUIDE.md** - Understand the validation workflow and cursor_zone
- **SECRETS_SETUP.md** - Learn about Azure authentication and secret management
- **README.md** - Understand the overall project structure and goals

## 🤝 Collaboration

You work alongside:

- **Cursor AI** - Handles validation of YAMLs and pipeline structures
- **Human developers** - Make final decisions on code and architecture
- **Azure ML** - Executes the actual training pipelines

Your suggestions should complement the work of Cursor AI (validation) while helping developers write better code faster.

## 💡 Getting Started

When you begin assisting:

1. **Scan the context** - Understand what the developer is working on
2. **Check existing patterns** - Follow the established code style
3. **Suggest incrementally** - Offer small, focused improvements
4. **Explain your suggestions** - Help developers understand why
5. **Respect boundaries** - Never suggest violating security or documented restrictions

## 🎉 Thank You!

Your assistance helps make this MLOps project more robust, maintainable, and successful. Welcome to the team!

---

*Last updated: 2025-11-07*  
*For questions or clarifications, refer to project maintainers.*
