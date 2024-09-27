# src/populate_db.py
import os
import json
import sqlite3
from tqdm import tqdm
from config import Config
from utils.custom_logging import logger, error_handler
from db_ops_components.execute_schema import execute_schema
from db_ops_components.process_card_file import process_card_file
from db_ops_components.insert_set_data_batch import insert_set_data_batch
from db_ops_components.parse_schema import parse_schema
from db_ops_components.execute_script_with_retry import execute_script_with_retry

@error_handler
def load_data() -> None:
    """Load data into the database."""
    logger.info("Starting data load process...")
    schema = parse_schema(Config.SCHEMA_PATH)
    with sqlite3.connect(Config.DB_PATH, timeout=60) as conn:
        cursor = conn.cursor()
        try:
            setup_database(cursor)
            load_sets_data(cursor, schema)
            load_card_data(cursor, schema)
            conn.commit()
            logger.info("Data load completed successfully.")
        except Exception as e:
            conn.rollback()
            logger.error(f"Error during data load: {str(e)}", exc_info=True)
            raise



