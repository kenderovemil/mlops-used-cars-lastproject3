#!/usr/bin/env python3
"""
Run pipeline with local CSV file bundled in code directory
"""
from azure.ai.ml import MLClient, Input
from azure.ai.ml.dsl import pipeline
from azure.ai.ml.entities import PipelineJob
from azure.identity import DefaultAzureCredential
import shutil
import os

# Initialize MLClient
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="77c91b3f-d78c-4832-8ed2-a5dd9c501e0e",
    resource_group_name="streaming_autovehicle_pricing_MLOPS",
    workspace_name="project_III_MLOPS"
)

# Create a data directory in the pipeline folder
pipeline_dir = "/home/azureuser/cloudfiles/code/Users/kenderov.emil/mlops/azureml/train"
data_dir = os.path.join(pipeline_dir, "data")
os.makedirs(data_dir, exist_ok=True)

# Copy CSV to pipeline data directory
source_csv = "/home/azureuser/cloudfiles/code/Users/kenderov.emil/data/used_cars.csv"
dest_csv = os.path.join(data_dir, "used_cars.csv")
shutil.copy2(source_csv, dest_csv)
print(f"✓ Copied CSV to {dest_csv}")

# Load registered components
prep_component = ml_client.components.get("prep_component", version="3")
train_component = ml_client.components.get("train_model_component", version="3")
register_component = ml_client.components.get("register_component", version="3")

@pipeline(
    display_name="SkyCore Pipeline - Local CSV",
    description="Pipeline using local CSV file bundled with code"
)
def skycore_pipeline(training_data):
    # Step 1: Data preparation
    prep_job = prep_component(raw_data=training_data)
    prep_job.compute = "cpu-cluster"
    
    # Step 2: Model training
    train_job = train_component(
        train_data=prep_job.outputs.train_data,
        test_data=prep_job.outputs.test_data,
        n_estimators=200,
        max_depth=10
    )
    train_job.compute = "cpu-cluster"
    
    # Step 3: Model registration
    register_job = register_component(
        model_name="skycore_rf_model",
        model_path=train_job.outputs.model_output
    )
    register_job.compute = "cpu-cluster"
    
    return {
        "train_data": prep_job.outputs.train_data,
        "test_data": prep_job.outputs.test_data,
        "model_output": train_job.outputs.model_output,
        "model_info": register_job.outputs.model_info_output_path
    }

# Create pipeline instance with local file input
pipeline_job = skycore_pipeline(
    training_data=Input(type="uri_file", path=dest_csv)
)

# Submit pipeline
print("\n🚀 Submitting pipeline...")
returned_job = ml_client.jobs.create_or_update(pipeline_job)

print(f"\n✅ Pipeline submitted successfully!")
print(f"📦 Job name: {returned_job.name}")
print(f"📊 Status: {returned_job.status}")
print(f"🔗 Studio URL: {returned_job.studio_url}")
