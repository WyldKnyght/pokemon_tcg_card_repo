# src\config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Root Folder
    PROJECT_ROOT = os.getenv('PROJECT_ROOT')

    # Application Entrypoint
    ENTRY_POINT = os.getenv('ENTRY_POINT')

    # Database
    DB_PATH = os.getenv('DB_PATH')
    SCHEMA_PATH = os.getenv('SCHEMA_PATH')

    # GitHub Repository
    REPO_PATH = os.getenv('REPO_PATH')

    # Data directories
    CARDS_DATA_DIR = os.getenv('CARDS_DATA_DIR')
    SETS_DATA_PATH = os.getenv('SETS_DATA_PATH')

    # Define the allowed set IDs (leave blank to include all sets)
    ALLOWED_SET_IDS = ""