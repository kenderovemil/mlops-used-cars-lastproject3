<<<<<<< HEAD
# Used Cars MLOps Project

This is the initial structure.
=======
# mlops-used-cars-mirror
Used Cars Modeling
🚗 Used Cars Pricing MLOps Pipeline
This repository contains an end-to-end MLOps pipeline for predicting used car prices, designed for an automobile dealership in Las Vegas. The pipeline automates data preparation, model training, evaluation, registration, and CI/CD deployment using Azure Machine Learning and GitHub Actions.

📌 Problem Statement
Problem Statement: An automobile dealership in Los Vegas specializes in selling luxury and non-luxury vehicles. They cater to diverse customer preferences with varying vehicle specifications, such as mileage, engine capacity, and seating capacity. However, the dealership faces significant challenges in maintaining consistency and efficiency across its pricing strategy due to reliance on manual processes and disconnected systems. Pricing evaluations are prone to errors, updates are delayed, and scaling operations are difficult as demand grows. These inefficiencies impact revenue and customer trust. Recognizing the need for a reliable and scalable solution, the dealership is seeking to implement a unified system that ensures seamless integration of data-driven pricing decisions, adaptability to changing market conditions, and operational efficiency.

🎯 Objective
The dealership has hired you as an MLOps Engineer to design and implement an MLOps pipeline that automates the pricing workflow. This pipeline will encompass data cleaning, preprocessing, transformation, model building, training, evaluation, and registration with CI/CD capabilities to ensure continuous integration and delivery. Your role is to overcome challenges such as integrating disparate data sources, maintaining consistent model performance, and enabling scalable, automated updates to meet evolving business needs. The expected outcomes are a robust, automated system that improves pricing accuracy, operational efficiency, and scalability, driving increased profitability and customer satisfaction.

📊 Dataset Description
Feature	Description
Segment	Luxury or non-luxury vehicle classification
Kilometers_Driven	Total kilometers driven
Mileage	Fuel efficiency (km/l)
Engine	Engine capacity (cc)
Power	Engine power (BHP)
Seats	Number of seats
Price	Vehicle price in lakhs (₹100,000 units)
🧪 Pipeline Components
Data Preparation (prepare.py)

Reads raw CSV
Splits into train/test
Writes outputs and diagnostics
Model Training (train_model.py)

Trains Random Forest Regressor
Logs MSE in MLflow
Saves model as MLflow artifact
Model Registration (model_register.py)

Loads best model
Registers in MLflow registry
End-to-End Workflow (pipeline_definition.py)

Assembles all steps into a unified pipeline
Executes in AzureML Studio
⚙️ Technologies Used
Azure Machine Learning
MLflow
GitHub Actions
Python (pandas, scikit-learn)
YAML for CI/CD workflows
🚀 How to Run
Clone the repo
Configure AzureML workspace
Run prepare.py locally or via AzureML
Submit training and registration jobs
Trigger GitHub Actions workflow for CI/CD
📂 Folder Structure
├── Week-17_Project_FullCode_Notebook .ipynb ├── data │ └── used_cars.csv ├── data-science │ ├── components │ │ ├── prep_component.yml │ │ ├── prep_component.yml.amltmp │ │ ├── prep_job.yml │ │ └── prep_job.yml.amltmp │ ├── environment │ │ ├── train-conda.yml.amltmp │ │ ├── train_conda.yml │ │ └── train_conda.yml.amltmp │ └── src │ ├── prep.py │ ├── prep.py.amltmp │ ├── prepare.py │ ├── prepare.py.amltmp │ ├── register.py │ ├── register.py.amltmp │ ├── train.py │ └── train.py.amltmp ├── downloaded_outputs_<ИМЕТО_НА_JOB-А> ├── downloaded_outputs_tough_tail_fg4r05lw6k ├── env ├── github_working │ ├── custom-create-compute.yml │ ├── custom-register-dataset.yml │ ├── custom-register-environment.yml │ ├── custom-run-pipeline.yml │ └── deploy-model-training-pipeline-classical.yml ├── mlops │ └── azureml │ └── train │ ├── data.yml │ ├── newpipeline.yml │ ├── newpipeline.yml.amltmp │ ├── prep.yml │ ├── prep.yml.amltmp │ ├── register.yml │ ├── register.yml.amltmp │ ├── train-env.yml │ ├── train-env.yml.amltmp │ ├── train.yml │ └── train.yml.amltmp ├── model_training │ ├── train_model.py │ └── train_model.py.amltmp ├── notes │ └── notes ├── outputs │ ├── model │ │ ├── MLmodel │ │ ├── conda.yaml │ │ ├── model.pkl │ │ ├── python_env.yaml │ │ └── requirements.txt │ ├── model_info │ │ └── model_info.json │ ├── test │ │ └── test.csv │ └── train │ └── train.csv ├── outputs_cool_market_ptblwpcn61 │ └── artifacts │ ├── outputs │ │ ├── prep_diagnostics.json │ │ ├── test │ │ │ └── test.csv │ │ └── train │ │ └── train.csv │ ├── system_logs │ │ ├── cs_capability │ │ │ └── cs-capability.log │ │ ├── data_capability │ │ │ ├── data-capability.log │ │ │ └── rslex.log.2025-10-28-16 │ │ ├── hosttools_capability │ │ │ └── hosttools-capability.log │ │ ├── lifecycler │ │ │ ├── execution-wrapper.log │ │ │ └── lifecycler.log │ │ ├── metrics_capability │ │ │ └── metrics-capability.log │ │ └── snapshot_capability │ │ └── snapshot-capability.log │ └── user_logs │ └── std_log.txt ├── prep_job.yml ├── prep_job.yml.bak ├── prep_job_fixed.yml ├── prep_outputs │ └── artifacts │ └── system_logs │ ├── cs_capability │ │ └── cs-capability.log │ ├── data_capability │ │ ├── data-capability.log │ │ └── rslex.log.2025-10-27-17 │ ├── hosttools_capability │ │ └── hosttools-capability.log │ ├── lifecycler │ │ ├── execution-wrapper.log │ │ └── lifecycler.log │ ├── metrics_capability │ │ └── metrics-capability.log │ └── snapshot_capability │ └── snapshot-capability.log ├── prep_outputs_debug │ └── artifacts │ └── system_logs │ ├── cs_capability │ │ └── cs-capability.log │ ├── data_capability │ │ ├── data-capability.log │ │ └── rslex.log.2025-10-28-15 │ ├── hosttools_capability │ │ └── hosttools-capability.log │ ├── lifecycler │ │ ├── execution-wrapper.log │ │ └── lifecycler.log │ ├── metrics_capability │ │ └── metrics-capability.log │ └── snapshot_capability │ └── snapshot-capability.log ├── prep_outputs_fixed ├── prep_outputs_manual │ └── artifacts │ ├── system_logs │ │ ├── cs_capability │ │ │ └── cs-capability.log │ │ ├── data_capability │ │ │ ├── data-capability.log │ │ │ └── rslex.log.2025-10-28-15 │ │ ├── hosttools_capability │ │ │ └── hosttools-capability.log │ │ ├── lifecycler │ │ │ ├── execution-wrapper.log │ │ │ └── lifecycler.log │ │ ├── metrics_capability │ │ │ └── metrics-capability.log │ │ └── snapshot_capability │ │ └── snapshot-capability.log │ └── user_logs │ └── std_log.txt ├── prep_outputs_py │ └── artifacts │ └── system_logs │ ├── cs_capability │ │ └── cs-capability.log │ ├── data_capability │ │ ├── data-capability.log │ │ └── rslex.log.2025-10-27-17 │ ├── hosttools_capability │ │ └── hosttools-capability.log │ ├── lifecycler │ │ ├── execution-wrapper.log │ │ └── lifecycler.log │ ├── metrics_capability │ │ └── metrics-capability.log │ └── snapshot_capability │ └── snapshot-capability.log ├── prep_outputs_safe │ └── artifacts │ ├── system_logs │ │ ├── cs_capability │ │ │ └── cs-capability.log │ │ ├── data_capability │ │ │ ├── data-capability.log │ │ │ └── rslex.log.2025-10-27-18 │ │ ├── hosttools_capability │ │ │ └── hosttools-capability.log │ │ ├── lifecycler │ │ │ ├── execution-wrapper.log │ │ │ └── lifecycler.log │ │ ├── metrics_capability │ │ │ └── metrics-capability.log │ │ └── snapshot_capability │ │ └── snapshot-capability.log │ └── user_logs │ └── std_log.txt ├── tmp_test │ └── test.csv ├── tmp_train │ ├── prep_diagnostics.json │ └── train.csv ├── used-cars-mlops │ └── README.md └── week-17_project_fullcode_notebook .ipynb.amltmp

📸 Screenshots
✅ AzureML pipeline execution
✅ GitHub Actions workflow run
✅ Sample outputs and diagnostics
🔗 Links
AzureML Studio Pipeline Run
GitHub Actions Workflow
📈 Business Impact
Improved pricing accuracy
Faster updates and scalability
Increased customer trust and profitability
🧠 Author
Emil Kenderov — AI student
>>>>>>> ba77a79c1622b0058c61ec714b97e0fe64a74bab
