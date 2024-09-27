# src/db_ops_components/check_tables.py

import sqlite3
from utils.custom_logging import logger, error_handler

@error_handler
def check_tables(cursor: sqlite3.Cursor) -> None:
    """Check if all tables have been created correctly."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    logger.info(f"Existing tables: {', '.join(table_names)}")
