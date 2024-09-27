# src/db_ops_components/execute_insert.py
import sqlite3
from typing import List
from utils.custom_logging import logger

def execute_insert(cursor: sqlite3.Cursor, insert_statement: str, data: List[tuple], table: str) -> None:
    try:
        cursor.executemany(insert_statement, data)
    except sqlite3.Error as e:
        logger.error(f"Error inserting data into {table}: {e}")
        logger.debug(f"Insert statement: {insert_statement}")
        logger.debug(f"First row of data: {data[0] if data else 'No data'}")
        raise