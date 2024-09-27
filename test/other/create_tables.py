# src/db_ops_components/create_tables.py

from utils.custom_logging import logger, error_handler
from .connection_pool import get_db_connection
from .execute_schema import execute_schema

@error_handler
def create_tables() -> None:
    """Create the database and tables using the schema.sql file if they don't exist."""
    logger.info("Updating database schema...")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        execute_schema(cursor)

    logger.info("Database schema update completed.")