# src\configs\env_settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EnvSettings:
    # Root Folder
    PROJECT_ROOT = os.getenv('PROJECT_ROOT')

    # Application Entrypoint
    ENTRY_POINT = os.getenv('ENTRY_POINT')

    # Database
    DB_PATH = os.getenv('DB_PATH')
    SCHEMA_PATH = os.getenv('SCHEMA_PATH')

    # GitHub Repository
    REPO_PATH = os.getenv('REPO_PATH')
    GITHUB_MY_REPO = os.getenv('GITHUB_MY_REPO')

    # Pokemon TCG Data
    GITHUB_TCG_REPO = os.getenv('GITHUB_TCG_REPO')
    CARDS_DATA_DIR = os.getenv('CARDS_DATA_DIR')
    SETS_DATA_PATH = os.getenv('SETS_DATA_PATH')
    SETS_DATA_DIR = os.path.normpath(os.getenv('SETS_DATA_DIR'))

    # Define the allowed set IDs (leave blank to include all sets)
    ALLOWED_SET_IDS = ""
