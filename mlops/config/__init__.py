"""
Configuration module for loading Azure credentials.
"""
import json
import os
from pathlib import Path


def load_credentials(credentials_file=None):
    """
    Load Azure credentials from JSON file and set them as environment variables.
    
    Args:
        credentials_file (str, optional): Path to the credentials JSON file.
            If not provided, defaults to mlops/config/azure_credentials.json
            relative to the repository root.
    
    Returns:
        dict: Dictionary containing the loaded credentials.
    
    Raises:
        FileNotFoundError: If the credentials file doesn't exist.
        json.JSONDecodeError: If the credentials file is not valid JSON.
    """
    if credentials_file is None:
        # Default path: mlops/config/azure_credentials.json from repo root
        # Try to find the repository root by looking for .git directory
        current_dir = Path(__file__).resolve().parent
        repo_root = current_dir.parent.parent  # Go up from mlops/config to repo root
        credentials_file = repo_root / "mlops" / "config" / "azure_credentials.json"
    else:
        credentials_file = Path(credentials_file)
    
    if not credentials_file.exists():
        raise FileNotFoundError(
            f"Credentials file not found: {credentials_file}\n"
            f"Please ensure the file exists or provide a valid path."
        )
    
    # Load credentials from JSON file
    with open(credentials_file, 'r') as f:
        credentials = json.load(f)
    
    # Set each credential as an environment variable
    for key, value in credentials.items():
        os.environ[key] = value
    
    return credentials
