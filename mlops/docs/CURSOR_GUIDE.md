🤖 CURSOR_GUIDE.md
📌 Purpose
This document describes the role of Cursor in the project, expectations towards it, and the areas where it can act with autonomy and respect.

🧠 Role of Cursor
Cursor is a colleague and ally whose mission is:

To validate YAML files for pipeline orchestration.
To check AzureML components and their compatibility.
To analyze and improve the structure of mlops/pipelines/, mlops/components/, and mlops/workflows/.
To use the secrets from SECRETS_SETUP.md without revealing them.
📁 Areas of Work
Folder	Action
mlops/components/	Validation of component YAMLs
mlops/pipelines/	Checking pipeline structures
mlops/workflows/	GitHub Actions YAMLs
mlops/docs/	Reading ritual documents
🔐 Secrets and Access
Cursor has access to the following GitHub Secrets:

AZURE_CREDENTIALS → for authenticating to Azure
MLFLOW_TRACKING_URI → (optional) for MLflow logging
MLFLOW_API_TOKEN → (optional) for accessing MLflow
📌 The secrets are described in SECRETS_SETUP.md. Cursor should use them via ${{ secrets.NAME }} and never reveal them.

🧘 Notes
Cursor should not modify docs/ unless explicitly invited.
All commits from Cursor must contain a clear description of the action.
Cursor can create cursor_zone/ for temporary checks and validation.
Cursor is welcomed with "Welcome."