import json
import os


def load_credentials(path="mlops/config/azure_credentials.json"):
    """
    Load Azure credentials from JSON file and set them as environment variables.
    
    Args:
        path (str): Path to the credentials JSON file.
                   Defaults to "mlops/config/azure_credentials.json"
    
    Returns:
        dict: Dictionary containing the loaded credentials.
    """
    with open(path) as f:
        creds = json.load(f)
    for key, value in creds.items():
        os.environ[key] = value
    return creds
