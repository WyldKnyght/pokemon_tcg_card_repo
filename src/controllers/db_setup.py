# src/controllers/db_setup.py
import sqlite3
from config import Config
from utils.custom_logging import error_handler, logger

@error_handler
def execute_schema(cursor: sqlite3.Cursor) -> None:
    """Execute the SQL schema, silently skipping statements for tables that already exist."""
    with open(Config.SCHEMA_PATH, 'r') as schema_file:
        schema_script = schema_file.read()

    # Split the script into individual SQL statements
    statements = schema_script.split(';')

    for statement in statements:
        if statement := statement.strip():
            try:
                cursor.execute(statement)
            except sqlite3.OperationalError as e:
                if "already exists" not in str(e):
                    logger.error(f"Error executing schema statement: {e}")
                    raise

    logger.info("Schema execution completed.")

def setup_database(cursor):
    execute_schema(cursor)
