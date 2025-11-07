#!/usr/bin/env python3
"""
YAML Validation Helper for GitHub Copilot

This script helps validate YAML files for:
- Azure ML pipeline definitions
- Azure ML component definitions
- GitHub Actions workflows
- Conda environment files

Usage:
    python validate_yaml.py <file_path>
    python validate_yaml.py --all  # Validate all YAML files in the project

Example:
    python validate_yaml.py mlops/azureml/train/newpipeline.yml
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Tuple

try:
    import yaml
except ImportError:
    print("⚠️  PyYAML not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    import yaml


def validate_yaml_syntax(file_path: str) -> Tuple[bool, str]:
    """
    Validate YAML syntax for a given file.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True, "✅ YAML syntax is valid"
    except yaml.YAMLError as e:
        return False, f"❌ YAML syntax error: {e}"
    except Exception as e:
        return False, f"❌ Error reading file: {e}"


def check_azure_ml_schema(file_path: str, content: dict) -> List[str]:
    """
    Perform basic checks for Azure ML YAML files.
    
    Args:
        file_path: Path to the file
        content: Parsed YAML content
        
    Returns:
        List of validation messages
    """
    messages = []
    
    # Check for schema reference
    if '$schema' not in content:
        messages.append("⚠️  Missing '$schema' field (recommended for Azure ML YAMLs)")
    
    # Check for required fields based on type
    file_type = content.get('type', '')
    
    if file_type == 'pipeline':
        if 'jobs' not in content:
            messages.append("❌ Pipeline missing 'jobs' field")
        if 'display_name' not in content:
            messages.append("⚠️  Missing 'display_name' (recommended)")
            
    elif file_type == 'command':
        if 'command' not in content:
            messages.append("❌ Command component missing 'command' field")
        if 'name' not in content:
            messages.append("❌ Component missing 'name' field")
        if 'environment' not in content:
            messages.append("⚠️  Missing 'environment' field")
            
    # Check for inputs/outputs if defined
    if 'inputs' in content:
        for input_name, input_def in content['inputs'].items():
            if isinstance(input_def, dict) and 'type' not in input_def:
                messages.append(f"⚠️  Input '{input_name}' missing 'type' specification")
                
    if 'outputs' in content:
        for output_name, output_def in content['outputs'].items():
            if isinstance(output_def, dict) and 'type' not in output_def:
                messages.append(f"⚠️  Output '{output_name}' missing 'type' specification")
    
    return messages


def check_github_actions(content: dict) -> List[str]:
    """
    Perform basic checks for GitHub Actions workflow files.
    
    Args:
        content: Parsed YAML content
        
    Returns:
        List of validation messages
    """
    messages = []
    
    if 'name' not in content:
        messages.append("⚠️  Missing 'name' field (recommended)")
        
    if 'on' not in content:
        # Check if this is a reusable workflow (workflow_call)
        is_reusable = False
        if 'jobs' in content:
            for job_name, job_config in content.get('jobs', {}).items():
                if isinstance(job_config, dict):
                    # Reusable workflows don't need 'on' at top level
                    is_reusable = True
                    break
        
        if not is_reusable:
            messages.append("❌ Missing 'on' field (required for workflows)")
        else:
            messages.append("ℹ️  Appears to be a reusable workflow (workflow_call)")
        
    if 'jobs' not in content:
        messages.append("❌ Missing 'jobs' field")
        
    # Check for secrets references
    yaml_str = yaml.dump(content)
    if 'secrets.' in yaml_str:
        messages.append("ℹ️  Uses GitHub Secrets (ensure they are configured)")
    
    return messages


def check_conda_env(content: dict) -> List[str]:
    """
    Perform basic checks for Conda environment files.
    
    Args:
        content: Parsed YAML content
        
    Returns:
        List of validation messages
    """
    messages = []
    
    if 'name' not in content:
        messages.append("⚠️  Missing 'name' field")
        
    if 'dependencies' not in content:
        messages.append("❌ Missing 'dependencies' field")
        
    if 'channels' not in content:
        messages.append("⚠️  Missing 'channels' field (recommended)")
    
    return messages


def validate_file(file_path: str) -> bool:
    """
    Validate a single YAML file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if validation passed, False otherwise
    """
    print(f"\n📄 Validating: {file_path}")
    print("=" * 60)
    
    # Check syntax
    is_valid, message = validate_yaml_syntax(file_path)
    print(message)
    
    if not is_valid:
        return False
    
    # Load content for deeper validation
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ Could not load YAML: {e}")
        return False
    
    # Determine file type and run appropriate checks
    messages = []
    validation_type = None
    
    file_name = os.path.basename(file_path).lower()
    parent_dir = os.path.basename(os.path.dirname(file_path))
    
    # Check if content is a dictionary (some YAMLs might be lists or other types)
    if not isinstance(content, dict):
        messages.append("ℹ️  YAML content is not a dictionary")
        for msg in messages:
            print(msg)
        return True
    
    if 'workflow' in file_path or parent_dir == 'workflows':
        messages = check_github_actions(content)
        validation_type = "GitHub Actions Workflow"
    elif 'conda' in file_name or 'environment' in file_name:
        messages = check_conda_env(content)
        validation_type = "Conda Environment"
    elif content.get('type') in ['pipeline', 'command', 'sweep']:
        messages = check_azure_ml_schema(file_path, content)
        validation_type = f"Azure ML {content.get('type').title()}"
    
    # Print validation type
    if validation_type:
        print(f"ℹ️  Validated as: {validation_type}")
    
    # Print validation messages
    if messages:
        for msg in messages:
            print(msg)
    elif not validation_type:
        print("ℹ️  No specific validation rules applied")
    
    return True


def find_yaml_files(root_dir: str = '.') -> List[str]:
    """
    Find all YAML files in the project.
    
    Args:
        root_dir: Root directory to search from
        
    Returns:
        List of YAML file paths
    """
    yaml_files = []
    excluded_dirs = {'.git', 'node_modules', 'venv', 'env', '__pycache__', 'outputs', '.ipynb_checkpoints'}
    
    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        for file in files:
            if file.endswith(('.yml', '.yaml')) and not file.endswith('.amltmp'):
                yaml_files.append(os.path.join(root, file))
    
    return sorted(yaml_files)


def main():
    parser = argparse.ArgumentParser(
        description="Validate YAML files for Azure ML, GitHub Actions, and Conda",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate a single file
  python validate_yaml.py mlops/azureml/train/newpipeline.yml
  
  # Validate all YAML files
  python validate_yaml.py --all
  
  # Validate specific directory
  python validate_yaml.py --directory mlops/azureml/train
        """
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='Path to YAML file to validate'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Validate all YAML files in the project'
    )
    parser.add_argument(
        '--directory',
        help='Validate all YAML files in a specific directory'
    )
    
    args = parser.parse_args()
    
    # Determine which files to validate
    files_to_validate = []
    
    if args.all:
        print("🔍 Finding all YAML files...")
        files_to_validate = find_yaml_files()
    elif args.directory:
        if not os.path.isdir(args.directory):
            print(f"❌ Directory not found: {args.directory}")
            sys.exit(1)
        print(f"🔍 Finding YAML files in {args.directory}...")
        files_to_validate = find_yaml_files(args.directory)
    elif args.file:
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        files_to_validate = [args.file]
    else:
        parser.print_help()
        sys.exit(1)
    
    if not files_to_validate:
        print("⚠️  No YAML files found")
        sys.exit(0)
    
    print(f"📋 Found {len(files_to_validate)} YAML file(s) to validate")
    
    # Validate each file
    all_valid = True
    for file_path in files_to_validate:
        if not validate_file(file_path):
            all_valid = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ All YAML files validated successfully!")
        sys.exit(0)
    else:
        print("❌ Some YAML files have issues")
        sys.exit(1)


if __name__ == "__main__":
    main()
