# Action Plan – Azure Login Failures

## Step 1 – YAML Corrections (azure/login usage)
- Bump every workflow to `azure/login@v2` (`deploy-model-training-pipeline-classical.yml`, all `custom-*.yml`, `github_workflows/azureml-pipeline.yml`).
- Remove the explicit `auth-type` parameter so the action performs workload identity federation automatically; if policy requires the field, set `auth-type: SERVICE_PRINCIPAL` after the upgrade.
- In reusable workflows, either delete the `auth-type` input or mark it `required: true` with `default: SERVICE_PRINCIPAL` to keep callers aligned.
- Commit the YAML changes together to simplify review and rollback.

## Step 2 – Federated Credential Verification
- Run `az ad app federated-credential list --id <AZURE_CLIENT_ID>` and confirm subjects for `repo:kenderovemil/mlops-used-cars-lastproject3:ref:refs/heads/main` and `repo:kenderovemil/mlops-used-cars-lastproject3:pull_request` (plus any extra contexts you need).
- If mismatches appear, update the App Registration in Azure AD to match the active triggers before retrying the workflow.
- Record the final credential set in the team wiki or `/mlops/docs/` for future audits.

## Step 3 – Python SDK Fallback Option
- Validate the existing scripts in `mlops/scripts/` (`create_compute.py`, `register_dataset.py`, `register_environment.py`, `run_pipeline.py`) using the upgraded login session.
- If CLI issues persist, prepare workflow steps that call these scripts directly instead of `az ml ...`, ensuring env vars `AZURE_SUBSCRIPTION_ID`, `RESOURCE_GROUP`, and `WORKSPACE_NAME` are exported.
- Capture any missing package dependencies in a dedicated `requirements-dev.txt` or inline `pip install` step.

## Step 4 – Validation & Logging
- Trigger `deploy-model-training-pipeline-classical.yml` from both a push to `main` and a PR branch; confirm the Azure Login step logs "Login using Workload Identity Federation" and that downstream steps succeed.
- Add the temporary "Debug context" step (if needed) to echo branch/event/secrets presence, then remove it once diagnostics finish.
- Save the Azure Login step excerpt from the first successful run to `ai_reviews/log_extracts/azure_login_debug.txt` for traceability.
- Close the incident after two consecutive green runs (push + PR) and document the outcome in the repository changelog.
