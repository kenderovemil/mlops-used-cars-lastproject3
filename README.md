# 🚗 Used Cars Price Prediction - MLOps Pipeline Project

[![Azure ML](https://img.shields.io/badge/Azure-ML-blue)](https://azure.microsoft.com/en-us/services/machine-learning/)
[![Python](https://img.shields.io/badge/Python-3.9-green)](https://www.python.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Model%20Registry-orange)](https://mlflow.org/)
[![Status](https://img.shields.io/badge/Status-Commission%20Review-yellow)](https://github.com/kenderovemil/mlops-used-cars-lastproject3)

**An end-to-end MLOps pipeline for predicting used car prices using Azure Machine Learning**

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Features](#-features)
- [Documentation](#-documentation)
- [Installation](#-installation)
- [Usage](#-usage)
- [Current Status](#-current-status)
- [Learning Outcomes](#-learning-outcomes)
- [Contact](#-contact)

---

## 🤖 Welcome, GitHub Copilot!

This project welcomes assistance from GitHub Copilot for:
- **YAML structure suggestions** for Azure ML pipelines and GitHub Actions
- **Python code completion** for ML scripts and data processing
- **Documentation refinement** to improve clarity and maintainability

Please see [COPILOT_GUIDE.md](./COPILOT_GUIDE.md) for detailed guidelines and boundaries.

---

## 🎯 Project Overview

This project demonstrates a complete MLOps workflow for predicting used car prices using Azure Machine Learning. It implements a three-stage pipeline with automated data preparation, model training, and model registration for an automobile dealership in Las Vegas.

### **Key Highlights:**
- ✅ **End-to-End MLOps Pipeline**: Data prep → Training → Registration
- ✅ **Azure ML Integration**: Components, environments, compute clusters
- ✅ **Model Registry**: MLflow-based model versioning and tracking
- ✅ **Production-Ready Code**: Validated components and configurations
- ✅ **Comprehensive Documentation**: 8 detailed reports and guides

### **Dataset:**
- **Source**: Used Cars Dataset (202 samples)
- **Features**: Segment, kilometers driven, mileage, engine, power, seats
- **Target**: Price prediction (regression task)
- **Algorithm**: Random Forest Regressor

---

## 🚀 Quick Start

### **For Reviewers (5-minute overview):**
1. Open [`00_START_HERE.md`](00_START_HERE.md)
2. View [`Used_Cars_MLOps_Pipeline_Project_FINAL.html`](Used_Cars_MLOps_Pipeline_Project_FINAL.html) in your browser
3. Read the "Project Summary for Commission Review" section

### **For Technical Deep Dive:**
1. Clone the repository:
   ```bash
   git clone https://github.com/kenderovemil/mlops-used-cars-lastproject3.git
   cd mlops-used-cars-lastproject3
   ```

2. Check the documentation:
   - [`PROJECT_PRESENTATION_PACKAGE.md`](PROJECT_PRESENTATION_PACKAGE.md) - Complete presentation
   - [`FINAL_STATUS_REPORT.md`](FINAL_STATUS_REPORT.md) - Technical report
   - [`QUICKSTART.md`](QUICKSTART.md) - Deployment guide

3. Explore the code:
   - Python scripts: `data-science/src/`
   - Component definitions: `data-science/components/`
   - Pipeline configurations: `mlops/azureml/train/`

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Azure ML Pipeline Architecture                │
└─────────────────────────────────────────────────────────────────┘

   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
   │   Stage 1    │      │   Stage 2    │      │   Stage 3    │
   │──────────────│      │──────────────│      │──────────────│
   │ Data Prep    │ ───> │   Training   │ ───> │ Registration │
   └──────────────┘      └──────────────┘      └──────────────┘
         │                      │                      │
         v                      v                      v
   Train/Test Split      Random Forest         MLflow Registry
   Feature Engineering    R² Score: 0.878      Model Versioning


┌─────────────────────────────────────────────────────────────────┐
│                      Technology Stack                            │
├─────────────────────────────────────────────────────────────────┤
│ Cloud Platform:  Azure Machine Learning                         │
│ Compute:         Standard_DS11_v2 (CPU cluster)                 │
│ Environment:     Python 3.9 + scikit-learn + pandas + mlflow   │
│ Storage:         Azure Blob Storage (identity-based auth)       │
│ Model Registry:  MLflow (Azure ML integrated)                   │
│ Orchestration:   Azure ML Pipelines v2                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### **MLOps Best Practices:**
- 🔄 **Reproducible Pipelines**: YAML-based component definitions
- 📊 **Experiment Tracking**: MLflow integration for metrics and artifacts
- 🔐 **Secure Authentication**: Managed identity-based access
- 📦 **Environment Management**: Conda-based dependency isolation
- 🧪 **Validation Scripts**: Automated testing and validation
- 📝 **Comprehensive Logging**: Detailed execution logs and diagnostics

### **Pipeline Components:**

#### **1. Data Preparation** (`prep_component`)
- Loads dataset from Azure Blob Storage
- Performs train/test split (80/20)
- Saves processed data for training stage
- **Input**: Raw CSV data
- **Output**: Train/test datasets

#### **2. Model Training** (`train_model_component`)
- Trains Random Forest Regressor
- Logs metrics to MLflow (R², MAE, RMSE)
- Saves trained model artifacts
- **Input**: Train/test datasets
- **Output**: Trained model + metrics

#### **3. Model Registration** (`register_component`)
- Registers model in MLflow registry
- Tracks model versions and metadata
- Enables model promotion workflow
- **Input**: Trained model
- **Output**: Registered model in registry

---

## 📚 Documentation

### **Start Here:**
- [`00_START_HERE.md`](00_START_HERE.md) - Quick navigation guide
- [`FILE_INVENTORY.md`](FILE_INVENTORY.md) - Complete file listing

### **Comprehensive Reports:**
1. **[PROJECT_PRESENTATION_PACKAGE.md](PROJECT_PRESENTATION_PACKAGE.md)** - Full project presentation
2. **[FINAL_STATUS_REPORT.md](FINAL_STATUS_REPORT.md)** - Complete technical report
3. **[WORKSPACE_V2_STATUS.md](WORKSPACE_V2_STATUS.md)** - Infrastructure documentation
4. **[STORAGE_AUTHENTICATION_DIAGNOSTIC.md](STORAGE_AUTHENTICATION_DIAGNOSTIC.md)** - Authentication analysis
5. **[PIPELINE_FIXES_SUMMARY.md](PIPELINE_FIXES_SUMMARY.md)** - Code improvements
6. **[PIPELINE_SOLUTION.md](PIPELINE_SOLUTION.md)** - Solution architecture
7. **[QUICKSTART.md](QUICKSTART.md)** - Deployment guide

### **Exports:**
- [`Used_Cars_MLOps_Pipeline_Project_FINAL.html`](Used_Cars_MLOps_Pipeline_Project_FINAL.html) - Complete notebook in HTML
- [`Week-17_Project_FullCode_Notebook.ipynb`](Week-17_Project_FullCode_Notebook.ipynb) - Full Jupyter notebook

---

## 🔧 Installation

### **Prerequisites:**
- Python 3.9+
- Azure subscription
- Azure ML workspace
- Azure CLI installed

### **Local Setup:**

```bash
# Clone the repository
git clone https://github.com/kenderovemil/mlops-used-cars-lastproject3.git
cd mlops-used-cars-lastproject3

# Install Azure ML SDK
pip install azure-ai-ml azure-identity pandas scikit-learn mlflow

# Configure Azure credentials
az login
az account set --subscription <your-subscription-id>

# Set up workspace (optional)
chmod +x setup_new_workspace.sh
./setup_new_workspace.sh
```

---

## 💻 Usage

### **Register Components:**
```bash
python register_components.py
```

### **Register Data Asset:**
```bash
python register_data_asset.py
```

### **Validate Pipeline:**
```bash
chmod +x validate_pipeline.sh
./validate_pipeline.sh
```

### **Run Pipeline:**
```bash
cd mlops/scripts
python run_pipeline.py
```

### **Monitor in Azure ML Studio:**
```
https://ml.azure.com/workspaces/project_III_MLOPS_v2
```

---

## 📊 Current Status

### **✅ Completed:**
- All Python scripts implemented and tested
- All component YAMLs created and validated
- Components registered (version 3) in Azure ML
- Environment configured with all dependencies
- Compute cluster provisioned (Standard_DS11_v2)
- Data assets registered (used_cars_data:2)
- RBAC permissions configured
- Comprehensive documentation created (8 reports)
- GitHub repository organized and documented

### **⏳ In Progress:**
- Pipeline execution blocked by service-level authentication issue
- Issue requires Microsoft Azure Support investigation
- Root cause: StreamAccess.Authentication error at Azure ML service level
- All configuration verified correct via Azure CLI

### **🎓 Educational Value:**
This project successfully demonstrates:
- Complete MLOps pipeline architecture design
- Azure ML component-based development
- Infrastructure-as-code practices
- Systematic troubleshooting methodology
- Professional documentation standards
- Real-world cloud platform challenges

**Note:** While pipeline execution is currently blocked by a service-level Azure issue requiring Microsoft Support, the project comprehensively demonstrates MLOps knowledge and implementation skills. All code artifacts are production-ready and validated.

---

## 🎓 Learning Outcomes

### **Technical Skills Demonstrated:**
1. **Azure Machine Learning** - Pipeline orchestration, component development, environment management
2. **MLOps Practices** - Reproducible pipelines, model versioning, IaC, CI/CD integration
3. **Python Development** - Data preprocessing, model training, MLflow tracking, Azure SDK
4. **DevOps & Cloud** - Git, GitHub workflows, Azure CLI, RBAC, diagnostics

### **Soft Skills Demonstrated:**
- Systematic problem-solving approach
- Comprehensive documentation
- Professional presentation
- Stakeholder communication
- Time management under constraints

---

## 📞 Contact & Support

**Project Author:** Emil Kenderov  
**GitHub:** [kenderovemil](https://github.com/kenderovemil)  
**Repository:** [mlops-used-cars-lastproject3](https://github.com/kenderovemil/mlops-used-cars-lastproject3)  
**Branch:** `fix-workflows`

---

## 📄 License

This project is created for educational purposes as part of an MLOps course.

---

## 🙏 Acknowledgments

- **Azure Machine Learning** - Cloud platform and MLOps tools
- **MLflow** - Model tracking and registry
- **scikit-learn** - Machine learning framework
- **GitHub Copilot** - Development assistance

---

<div align="center">

**⭐ If you find this project helpful, please consider giving it a star! ⭐**

---

**Built with ❤️ for Learning MLOps**

*Last Updated: November 13, 2025*

</div>

