from azure.ai.ml import command, Input
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient.from_config(credential=DefaultAzureCredential())

job = command(
    code="./src/model_training",
    command="python train_model.py --train_data ${{inputs.train_data}} --test_data ${{inputs.test_data}} --n_estimators 100 --max_depth 10 --model_output ${{outputs.model_output}}",
    inputs={
        "train_data": Input(path="azureml:used-cars-train:1", type="uri_file"),
        "test_data": Input(path="azureml:used-cars-test:1", type="uri_file")
    },
    outputs={
        "model_output": Input(type="uri_folder", mode="rw_mount")
    },
    environment="azureml:used-cars-env:1",
    compute="cpu-cluster",
    display_name="train-random-forest",
    description="Train Random Forest Regressor on used cars data"
)

ml_client.jobs.create_or_update(job)
