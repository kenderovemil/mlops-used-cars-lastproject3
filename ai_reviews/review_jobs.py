#!/usr/bin/env python3
"""
Script to review the last 5 jobs from Azure ML workspace.
Retrieves job information and saves it to markdown, CSV, and PDF formats.
"""

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from datetime import datetime
import os
import sys
import csv
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

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

def save_to_csv(jobs_data, output_path):
    """Save jobs data to CSV file."""
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Job ID', 'Display Name', 'Status', 'Dataset', 'Start Time', 'End Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for job in jobs_data:
                writer.writerow(job)
        
        print(f"✅ CSV file saved to: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving CSV file: {e}")
        return False

def save_to_pdf(jobs_data, output_path, workspace_name):
    """Save jobs data to PDF file."""
    try:
        # Create PDF document
        doc = SimpleDocTemplate(output_path, pagesize=landscape(letter))
        elements = []
        
        # Add title
        styles = getSampleStyleSheet()
        title = Paragraph(f"<b>Azure ML Jobs Review - {workspace_name}</b>", styles['Heading1'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Add generation date
        date_text = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        elements.append(date_text)
        elements.append(Spacer(1, 0.3*inch))
        
        # Prepare table data
        table_data = [['Job ID', 'Display Name', 'Status', 'Dataset', 'Start Time', 'End Time']]
        for job in jobs_data:
            table_data.append([
                job['Job ID'],
                job['Display Name'],
                job['Status'],
                job['Dataset'],
                job['Start Time'],
                job['End Time']
            ])
        
        # Create table
        table = Table(table_data, colWidths=[1.5*inch, 1.8*inch, 1*inch, 1.8*inch, 1.5*inch, 1.5*inch])
        
        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        print(f"✅ PDF file saved to: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving PDF file: {e}")
        import traceback
        traceback.print_exc()
        return False

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
        
        # Collect job data in a structured format
        jobs_data = []
        
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
        
        # Add each job to the table and collect data
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
            
            # Collect structured data for CSV and PDF
            jobs_data.append({
                'Job ID': job_id,
                'Display Name': display_name,
                'Status': status,
                'Dataset': dataset,
                'Start Time': start_time,
                'End Time': end_time
            })
            
            # Create markdown table row
            row = f"| {job_id} | {display_name} | {status} | {dataset} | {start_time} | {end_time} |"
            table_lines.append(row)
        
        # Output directory
        output_dir = os.path.dirname(__file__)
        
        # Save to Markdown
        md_output_path = os.path.join(output_dir, "jobs_review.md")
        with open(md_output_path, 'w') as f:
            f.write('\n'.join(table_lines))
        print(f"\n✅ Markdown file saved to: {md_output_path}")
        
        # Save to CSV
        csv_output_path = os.path.join(output_dir, "job_review.csv")
        save_to_csv(jobs_data, csv_output_path)
        
        # Save to PDF
        pdf_output_path = os.path.join(output_dir, "job_review.pdf")
        save_to_pdf(jobs_data, pdf_output_path, workspace_name)
        
        print(f"\n📊 Summary:")
        print(f"  - Markdown: {md_output_path}")
        print(f"  - CSV: {csv_output_path}")
        print(f"  - PDF: {pdf_output_path}")
        
        print(f"\nPreview of the markdown table:")
        print('\n'.join(table_lines))
        
    except Exception as e:
        print(f"❌ Error retrieving jobs: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
