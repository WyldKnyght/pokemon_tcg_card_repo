# src\utils\create_db_from_schema\create_database_from_schema.py
import sqlite3
from ..custom_logging import logger, error_handler

@error_handler
def validate_schema(conn: sqlite3.Connection, schema: str):
    """
    Validate the SQL schema by checking the syntax of each statement.

    Args:
        conn (sqlite3.Connection): The SQLite connection object.
        schema (str): The SQL schema string to validate.

    Raises:
        sqlite3.Error: If a syntax error is found in any SQL statement.
    """
    logger.info("Validating schema...")

    # Split the schema into individual statements using ';' as the delimiter
    for statement in schema.split(";"):
        # Strip any leading or trailing whitespace from the statement
        if statement := statement.strip():
            try:
                # Use EXPLAIN to check the syntax of the statement without executing it
                conn.execute(f"EXPLAIN {statement}")
            except sqlite3.Error as e:
                # Raise an error if the statement has a syntax error
                raise sqlite3.Error(f"Schema validation failed: {e} in statement: {statement}") from e

