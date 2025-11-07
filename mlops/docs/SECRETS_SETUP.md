📌 Purpose
This document describes all necessary GitHub Secrets for successful operation of GitHub Actions and Azure Machine Learning pipelines.

🧩 Required GitHub Secrets
Name	Type	Used by	Description
GH_TOKEN	String	Copilot	Personal GitHub token for API access and push/pull
AZURE_CREDENTIALS	JSON	Copilot	Service Principal for authentication to Azure
MLFLOW_TRACKING_URI	URI	Cursor	(optional) URI to MLflow server
MLFLOW_API_TOKEN	String	Cursor	(optional) Token for accessing MLflow server
🧭 How to Add Them
Go to GitHub → Settings → Secrets → Actions.
Click "New repository secret".
Enter the name and value.
Confirm.
 Notes
Never commit secrets in .ipynb, .py, or .yml.
Use secrets.NAME in GitHub Actions:
- name: Login to Azure
  uses: azure/login@v1
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}