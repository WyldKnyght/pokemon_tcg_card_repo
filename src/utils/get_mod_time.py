# src/controllers/db_modules/get_latest_modification_time.py
import os
from utils.custom_logging import get_update_logger

def get_latest_modification_time(directory):
    update_logger = get_update_logger()
    update_logger.debug(f"Checking directory: {directory}")

    if not os.path.exists(directory):
        update_logger.error(f"Directory does not exist: {directory}")
        return 0

    if not os.path.isdir(directory):
        update_logger.error(f"Path is not a directory: {directory}")
        return 0

    latest_time = 0
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    latest_time = max(latest_time, os.path.getmtime(file_path))

        if latest_time == 0:
            update_logger.warning(f"No JSON files found in directory: {directory}")

        return latest_time
    except Exception as e:
        update_logger.error(f"Error walking directory {directory}: {str(e)}", exc_info=True)
        return 0
