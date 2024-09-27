# src/db_ops_components/execute_query.py
import sqlite3
from utils.custom_logging import error_handler
from db_ops_components.execute_query_with_retry import execute_query_with_retry


@error_handler
def execute_query(cursor, query, params=None):
    try:
        """Execute a SQL query and return the results."""
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except sqlite3.OperationalError as e:
        if "database is locked" in str(e):
            # Retry the query after a short delay
            return execute_query_with_retry(cursor, query, params=params)
        else:
            raise
