# src/utils/create_db_from_schema/load_config.py
from pathlib import Path
import yaml
from typing import Dict, Any
from ..custom_logging import logger, error_handler

@error_handler
def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Load and validate configuration from YAML file.

    Args:
        config_path (Path): The path to the YAML file containing the configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the configuration settings.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration file is malformed or missing required keys.
    """
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

