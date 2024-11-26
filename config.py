"""
Configuration module for loading environment variables.

This module uses the `dotenv` package to load environment variables from a `.env` file if it exists.
Attributes:
    ENVIRONMENT (str): The environment in which the application is running. Defaults to 'PROD'.
    SETUP_SCHEMA (bool): A flag indicating whether to set up the schema. Defaults to False.
    CONGRESS (str): The congress number. Defaults to '118'.
    CONGRESS_API_KEY (str): The API key for accessing congress data.
"""
import os
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv(dotenv_path='.env', override=True)
    
ENVIRONMENT :str = os.getenv('ENVIRONMENT', 'PROD')
SETUP_SCHEMA :bool = os.getenv('SETUP_SCHEMA', False).lower() == 'true'
CONGRESS :str = os.getenv('CONGRESS', 118)
CONGRESS_API_KEY :str = os.getenv('CONGRESS_API_KEY')


if __name__ == "__main__":
    print(f"ENVIRONMENT: {ENVIRONMENT}")
