#!/usr/bin/env python3
"""
Script to review the last 5 jobs from Azure ML workspace.
Retrieves job information and saves it to a markdown table.
"""

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from datetime import datetime
import os
import sys

# Add parent directory to path to import utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mlops', 'scripts'))

try:
    from utils import load_credentials
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

def get_dataset_input(job):
    """Extract dataset input information from job inputs."""
    try:
        if hasattr(job, 'inputs') and job.inputs:
            for input_name, input_value in job.inputs.items():
                if input_value and hasattr(input_value, 'path'):
                    return input_value.path
                elif input_value:
                    return str(input_value)
        return "N/A"
    except Exception:
        return "N/A"

def format_datetime(dt):
    """Format datetime object to readable string."""
    if dt:
        if isinstance(dt, str):
            return dt
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"

def main():
    # Workspace configuration
    workspace_name = "project_III_MLOPS"
    
    # Try to load credentials from JSON file if available
    if UTILS_AVAILABLE:
        try:
            credentials_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'mlops', 
                'config', 
                'azure_credentials.json'
            )
            if os.path.exists(credentials_path):
                print(f"Loading credentials from {credentials_path}")
                # Note: This will only work if the file has actual values, not GitHub Actions templates
                load_credentials(credentials_path)
        except Exception as e:
            print(f"⚠️  Could not load credentials from file: {e}")
    
    # Get credentials from environment
    subscription_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
    resource_group = os.environ.get("RESOURCE_GROUP")
    
    if not subscription_id or not resource_group:
        print("⚠️  Warning: AZURE_SUBSCRIPTION_ID or RESOURCE_GROUP not set in environment.")
        print("Please set these environment variables before running this script.")
        print("\nExample:")
        print("  export AZURE_SUBSCRIPTION_ID='your-subscription-id'")
        print("  export RESOURCE_GROUP='your-resource-group'")
        sys.exit(1)
    
    # Create ML client with explicit parameters
    try:
        credential = DefaultAzureCredential()
        ml_client = MLClient(
            credential=credential,
            subscription_id=subscription_id,
            resource_group_name=resource_group,
            workspace_name=workspace_name
        )
        print(f"✅ Connected to workspace: {workspace_name}")
    except Exception as e:
        print(f"❌ Error: Could not initialize ML Client: {e}")
        sys.exit(1)
    
    print(f"📋 Retrieving jobs from workspace: {workspace_name}")
    
    # Get the last 5 jobs
    try:
        jobs_list = list(ml_client.jobs.list(max_results=5))
        
        if not jobs_list:
            print("⚠️  No jobs found in the workspace.")
            sys.exit(0)
        
        print(f"✅ Found {len(jobs_list)} jobs")
        
        # Prepare markdown table
        table_lines = [
            "# Azure ML Jobs Review",
            "",
            f"**Workspace:** {workspace_name}",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "| Job ID | Display Name | Status | Dataset | Start Time | End Time |",
            "|--------|--------------|--------|---------|------------|----------|"
        ]
        
        # Add each job to the table
        for job in jobs_list:
            job_id = job.name if hasattr(job, 'name') else "N/A"
            display_name = job.display_name if hasattr(job, 'display_name') else "N/A"
            status = job.status if hasattr(job, 'status') else "N/A"
            dataset = get_dataset_input(job)
            start_time = format_datetime(job.creation_context.created_at if hasattr(job, 'creation_context') else None)
            
            # Get end time from properties if available
            end_time = "N/A"
            if hasattr(job, 'properties') and job.properties and 'end_time' in job.properties:
                end_time = format_datetime(job.properties['end_time'])
            elif status in ["Completed", "Failed", "Canceled"]:
                # For completed jobs, try to get the last modified time
                if hasattr(job, 'creation_context') and hasattr(job.creation_context, 'last_modified_at'):
                    end_time = format_datetime(job.creation_context.last_modified_at)
            
            # Create table row
            row = f"| {job_id} | {display_name} | {status} | {dataset} | {start_time} | {end_time} |"
            table_lines.append(row)
        
        # Write to file
        output_path = os.path.join(os.path.dirname(__file__), "jobs_review.md")
        with open(output_path, 'w') as f:
            f.write('\n'.join(table_lines))
        
        print(f"\n✅ Jobs review saved to: {output_path}")
        print(f"\nPreview of the table:")
        print('\n'.join(table_lines))
        
    except Exception as e:
        print(f"❌ Error retrieving jobs: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
