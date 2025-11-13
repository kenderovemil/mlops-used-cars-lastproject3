# 🚀 Quick Start Guide - Azure ML Pipeline

## ✅ Status: All Components Registered Successfully!

Your pipeline is now ready to run. All components have been registered with version 3.

---

## 📦 Registered Components

✅ **prep_component:3** - Data preparation  
✅ **train_model_component:3** - Model training  
✅ **register_component:3** - Model registration  

✅ **Environment:** skycore-train-env-used-cars-mlops-v3:13  
✅ **Data Asset:** used_cars_raw:1  
✅ **Compute:** cpu-cluster  

---

## 🎯 Run Pipeline Now

### Option 1: Azure CLI (Recommended for Testing)

```bash
cd /home/azureuser/cloudfiles/code/Users/kenderov.emil

# Submit the pipeline
az ml job create \
  --file mlops/azureml/train/newpipeline.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS \
  --web
```

The `--web` flag will open Azure ML Studio in your browser to monitor the pipeline.

### Option 2: Python SDK

```python
from azure.ai.ml import MLClient, load_job
from azure.identity import DefaultAzureCredential

# Connect to workspace
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="77c91b3f-d78c-4832-8ed2-a5dd9c501e0e",
    resource_group_name="streaming_autovehicle_pricing_MLOPS",
    workspace_name="project_III_MLOPS"
)

# Load and submit pipeline
pipeline_job = load_job("mlops/azureml/train/newpipeline.yml")
submitted_job = ml_client.jobs.create_or_update(pipeline_job)

print(f"🔗 Studio URL: {submitted_job.studio_url}")
```

### Option 3: GitHub Actions

```bash
# Commit your changes
git add .
git commit -m "Pipeline v3 ready for production"
git push origin fix-workflows

# GitHub Actions will automatically:
# 1. Register components
# 2. Submit the pipeline
# 3. Monitor execution
```

---

## 🔍 Monitor Pipeline Execution

### Via Azure CLI
```bash
# Check job status
JOB_NAME="<your-job-name>"
az ml job show \
  --name $JOB_NAME \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS \
  --query status

# Stream logs
az ml job stream \
  --name $JOB_NAME \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS
```

### Via Azure ML Studio
Navigate to: https://ml.azure.com/  
→ Select workspace: `project_III_MLOPS`  
→ Go to: **Jobs** → Find your pipeline run

---

## 📊 Pipeline Steps

Your pipeline will execute in this order:

1. **prep_data** (prep_component:3)
   - Input: `used_cars_raw:1` (CSV file)
   - Output: `train_data/` and `test_data/` folders
   - Script: `data-science/src/prep.py`

2. **train_model** (train_model_component:3)
   - Input: `train_data/` and `test_data/` from step 1
   - Parameters: `n_estimators=200`, `max_depth=10`
   - Output: `model_output/` folder with trained model
   - Script: `data-science/src/train.py`

3. **register_model** (register_component:3)
   - Input: `model_output/` from step 2
   - Output: Registered model in Azure ML
   - Script: `data-science/src/register.py`

---

## 🧪 Test Individual Components Locally

Before running the full pipeline, you can test each component individually:

### Test Data Preparation
```bash
python data-science/src/prep.py \
  --raw_data data/used_cars_raw.csv \
  --train_data ./test_outputs/train \
  --test_data ./test_outputs/test
```

### Test Model Training
```bash
python data-science/src/train.py \
  --train_data ./test_outputs/train \
  --test_data ./test_outputs/test \
  --n_estimators 100 \
  --max_depth 10 \
  --model_output ./test_outputs/model
```

### Test Model Registration
```bash
python data-science/src/register.py \
  --model_name test_model \
  --model_path ./test_outputs/model \
  --model_info_output_path ./test_outputs/model_info
```

---

## ⚙️ Pipeline Configuration

### Input Data
- **Name:** used_cars_raw
- **Version:** 1
- **Type:** CSV file
- **Columns:** Segment, Kilometers_Driven, Mileage, Engine, Power, Seats, Price

### Training Parameters
You can modify these in `newpipeline.yml`:
- `n_estimators`: 200 (number of trees in random forest)
- `max_depth`: 10 (maximum depth of trees)

### Compute Configuration
- **Cluster:** cpu-cluster
- **VM Size:** Standard_DS11_v2
- **Min Instances:** 0
- **Max Instances:** 1

---

## 🔧 Troubleshooting

### Issue: Pipeline fails at prep_data step
**Check:** Ensure data asset `used_cars_raw:1` exists and is accessible
```bash
az ml data show --name used_cars_raw --version 1 \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS
```

### Issue: Pipeline fails at train_model step
**Check:** Review logs for data format issues
```bash
az ml job show --name <job-name> \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS \
  --query '{Status:status, Error:error}'
```

### Issue: Environment not found
**Solution:** The environment should already exist. If not:
```bash
az ml environment list \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS \
  --query "[?contains(name, 'skycore')]"
```

---

## 📈 Expected Output

Upon successful completion:

1. **Trained Model** will be saved in the pipeline outputs
2. **Model Registration** will create a new model version in Azure ML
3. **Metrics** including MSE and R² will be logged
4. **Model Info** will be available in the registered_model_info output

---

## 🎓 Next Steps After First Run

1. **Review Metrics:** Check model performance in Azure ML Studio
2. **Deploy Model:** Create an endpoint for real-time inference
3. **Schedule Pipeline:** Set up automated retraining on new data
4. **Monitor Performance:** Track model drift and data quality

---

## 📞 Need Help?

- **Azure ML Studio:** https://ml.azure.com/
- **Pipeline Documentation:** See `PIPELINE_FIXES_SUMMARY.md`
- **Validation Script:** Run `./validate_pipeline.sh`
- **Component Registration:** Run `python register_components.py`

---

**Ready to go! 🚀**

Run this command to start your first pipeline:

```bash
az ml job create \
  --file mlops/azureml/train/newpipeline.yml \
  --resource-group streaming_autovehicle_pricing_MLOPS \
  --workspace-name project_III_MLOPS \
  --web
```
