import os
from dotenv import load_dotenv
from pathlib import Path

class EnvConfig:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        
        # Assign environment variables to class attributes
        self.PROJECT_ROOT = Path(os.getenv('PROJECT_ROOT'))
        self.ENTRY_POINT = Path(os.getenv('ENTRY_POINT'))
        self.DB_PATH = Path(os.getenv('DB_PATH'))
        self.SCHEMA_PATH = Path(os.getenv('SCHEMA_PATH'))
        self.REPO_PATH = Path(os.getenv('REPO_PATH'))
        self.CARDS_DATA_DIR = Path(os.getenv('CARDS_DATA_DIR'))
        self.SETS_DATA_PATH = Path(os.getenv('SETS_DATA_PATH'))

    def validate_paths(self):
        """Validate that all paths exist"""
        for attr, path in self.__dict__.items():
            if isinstance(path, Path):
                if not path.exists():
                    print(f"Warning: {attr} path does not exist: {path}")

# Usage
config = EnvConfig()
config.validate_paths()

# Example of using the config
print(f"Project root: {config.PROJECT_ROOT}")
print(f"Database path: {config.DB_PATH}")
