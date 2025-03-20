# src/utils/create_db_from_schema/create_db_from_schema.py
from pathlib import Path
import sqlite3
import yaml
from sqlite3 import Error as SQLiteError
from typing import Dict, Any
from ..custom_logging import logger, setup_logging, error_handler

setup_logging()

def create_database_from_schema():
    """Create a SQLite database using a SQL schema file."""
    logger.info("Starting database creation process.")
    project_root = Path(__file__).parent.parent
    config_path = project_root / "utils" / "create_db_from_schema" / "user_variables.yaml"
    config = load_config(config_path)

    # Get the path to the database file and schema file
    db_path = project_root / config["DATA_DIR"] / config["DB_NAME"]
    schema_path = project_root / config["DATA_DIR"] / config["SCHEMA_NAME"]

    try:
        create_database(db_path, schema_path, overwrite=False)
        logger.info("Database creation/recreation completed successfully.")
    except FileNotFoundError as e:
        # Log file not found errors
        logger.error(f"File not found: {e}")
        raise
    except SQLiteError as e:
        # Log SQLite errors
        logger.error(f"SQLite error occurred: {e}")
        raise
    except ValueError as e:
        # Log configuration errors
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        # Log any other exceptions
        logger.error(f"An unexpected error occurred: {e}")
        raise

@error_handler
def create_database(db_path: Path, schema_path: Path, overwrite: bool = False):
    """Create a SQLite database using a SQL schema file."""
    logger.info(f"Creating database at {db_path}")

    if db_path.exists():
        if overwrite:
            logger.warning(f"Overwriting existing database at {db_path}")
            db_path.unlink()
        else:
            logger.warning(f"Database file already exists at {db_path}. Use overwrite=True to recreate.")
            return

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r') as schema_file:
            conn.executescript(schema_file.read())

    logger.info(f"Database {'recreated' if overwrite else 'created'} successfully at {db_path}")

@error_handler
def load_config(config_path: Path) -> Dict[str, Any]:
    """Load the configuration from a YAML file."""
    logger.info(f"Loading configuration from {config_path}")
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file: {e}") from e

    # Check that the config has the required keys
    required_keys = ["DATA_DIR", "DB_NAME", "SCHEMA_NAME"]
    if missing_keys := [key for key in required_keys if key not in config]:
        raise ValueError(f"Missing required configuration keys: {', '.join(missing_keys)}")

    # Validate that the values are strings
    for key in required_keys:
        if not isinstance(config[key], str):
            raise ValueError(f"Configuration key '{key}' must be a string")

    return config

if __name__ == "__main__":
    create_database_from_schema()

