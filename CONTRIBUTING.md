# 🚀 Quick Start Guide for Contributors

This guide helps you get started with contributing to the Used Cars MLOps project.

## 📖 Documentation Overview

Before making changes, please review these key documents:

1. **[COPILOT_GUIDE.md](./COPILOT_GUIDE.md)** - If you're using GitHub Copilot for assistance
2. **[CURSOR_GUIDE.md](./mlops/docs/CURSOR_GUIDE.md)** - If you're using Cursor AI for validation
3. **[SECRETS_SETUP.md](./SECRETS_SETUP.md)** - For configuring Azure credentials
4. **[README.md](./README.md)** - Project overview and structure

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- Azure subscription
- GitHub account with repository access
- Azure CLI installed

### Install Dependencies

```bash
# Install Python dependencies
pip install azure-ai-ml azure-identity pyyaml pandas scikit-learn

# Login to Azure
az login
```

### Configure Secrets

Follow the instructions in [SECRETS_SETUP.md](./SECRETS_SETUP.md) to set up:
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID
- AZURE_SUBSCRIPTION_ID

## 🧪 Development Workflow

### 1. Working with YAML Files

When creating or modifying YAML files:

```bash
# Validate a single YAML file
python validate_yaml.py mlops/azureml/train/newpipeline.yml

# Validate all YAML files in a directory
python validate_yaml.py --directory mlops/azureml/train

# Validate all YAML files in the project
python validate_yaml.py --all
```

### 2. Working with Python Scripts

Python scripts for MLOps are in:
- `data-science/src/` - Main ML scripts (prepare.py, train.py, register.py)
- `src/` - Additional utilities
- `mlops/cursor_zone/` - Validation scripts

When writing Python code:
- Follow existing patterns (see examples in COPILOT_GUIDE.md)
- Include proper error handling
- Add debug prints with `flush=True`
- Write diagnostic JSON files for tracking

### 3. Testing Changes Locally

Before pushing changes:

```bash
# Test data preparation
python data-science/src/prepare.py \
  --raw_data data/used_cars.csv \
  --test_size 0.2 \
  --random_state 42

# Check outputs
ls -la outputs/train/
ls -la outputs/test/
```

### 4. Using GitHub Copilot

If you're using GitHub Copilot:

✅ **DO:**
- Ask for YAML structure suggestions
- Request Python code completion
- Get help with documentation
- Follow security best practices

❌ **DON'T:**
- Hardcode secrets or credentials
- Modify cursor_zone/ without explicit permission
- Break existing working pipelines
- Remove error handling or logging

See [COPILOT_GUIDE.md](./COPILOT_GUIDE.md) for detailed guidelines.

### 5. Validation with Cursor AI

The `cursor_zone/` directory is reserved for validation tasks:

```bash
# Cursor AI can validate pipeline structures here
cd mlops/cursor_zone/
python cursor_check.py
```

See [CURSOR_GUIDE.md](./mlops/docs/CURSOR_GUIDE.md) for Cursor AI guidelines.

## 📂 Project Structure

```
mlops-used-cars-lastproject3/
├── data/                      # Raw data files
│   └── used_cars.csv
├── data-science/              # ML scripts and components
│   ├── src/                   # Python scripts
│   │   ├── prepare.py         # Data preparation
│   │   ├── train.py           # Model training
│   │   └── register.py        # Model registration
│   ├── components/            # Azure ML component YAMLs
│   └── environment/           # Conda environments
├── mlops/                     # MLOps configuration
│   ├── azureml/              # Azure ML definitions
│   │   └── train/            # Training pipeline YAMLs
│   ├── cursor_zone/          # Validation area (Cursor AI)
│   └── docs/                 # MLOps documentation
├── .github/workflows/         # CI/CD workflows
├── COPILOT_GUIDE.md          # GitHub Copilot guidelines
├── SECRETS_SETUP.md          # Azure secrets setup
├── validate_yaml.py          # YAML validation tool
└── README.md                 # Project overview
```

## 🔄 Contribution Process

1. **Read Documentation**
   - Review relevant guides (COPILOT_GUIDE.md, CURSOR_GUIDE.md)
   - Understand security requirements (SECRETS_SETUP.md)

2. **Make Changes**
   - Use GitHub Copilot for assistance if available
   - Follow existing code patterns
   - Validate YAML files with `validate_yaml.py`

3. **Test Locally**
   - Run scripts to ensure they work
   - Check for errors and fix issues
   - Validate output files

4. **Create Pull Request**
   - Include clear description of changes
   - Reference any related issues
   - Ensure CI/CD checks pass

5. **Validation**
   - Cursor AI may validate YAML structures
   - GitHub Actions will run automated tests
   - Code review by maintainers

## 🧪 Common Tasks

### Adding a New Pipeline Component

1. Create component YAML in `mlops/azureml/train/`
2. Define inputs, outputs, and command
3. Validate with `python validate_yaml.py <your-file>.yml`
4. Add to pipeline in `newpipeline.yml`
5. Test in cursor_zone if needed

### Updating Python Scripts

1. Make changes to scripts in `data-science/src/`
2. Test locally with sample data
3. Ensure error handling is robust
4. Update documentation if needed
5. Commit and push changes

### Modifying GitHub Actions

1. Edit workflows in `.github/workflows/`
2. Ensure secrets are referenced correctly
3. Validate YAML syntax
4. Test workflow by triggering it
5. Monitor workflow run in GitHub Actions

## 🆘 Getting Help

- **For YAML issues**: Check [COPILOT_GUIDE.md](./COPILOT_GUIDE.md) section on YAML structures
- **For Python issues**: Review examples in [COPILOT_GUIDE.md](./COPILOT_GUIDE.md)
- **For Azure setup**: See [SECRETS_SETUP.md](./SECRETS_SETUP.md)
- **For validation**: Use `validate_yaml.py` tool

## 🔐 Security Reminders

- **NEVER** commit secrets to the repository
- Always use `${{ secrets.NAME }}` in GitHub Actions
- Keep service principal credentials secure
- Rotate secrets regularly (every 90 days)
- Use least privilege access

## ✅ Checklist Before Committing

- [ ] Read relevant documentation guides
- [ ] Tested changes locally
- [ ] Validated YAML files
- [ ] No secrets in code
- [ ] Error handling in place
- [ ] Documentation updated if needed
- [ ] Clear commit message

---

Happy contributing! 🎉
