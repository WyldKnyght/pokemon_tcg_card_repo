# src/db_ops_components/check_set_data.py 
from utils.custom_logging import logger, error_handler
from db_ops_components.execute_query import execute_query

@error_handler
def check_set_data(cursor, set_id):
    """Check related tables for a specific set."""
    set_tables = ['set_legalities', 'set_images']

    for table in set_tables:
        related_data = execute_query(cursor, f'SELECT * FROM {table} WHERE set_id = ?', (set_id,))
        logger.info(f"{table} for set {set_id}:")
        for row in related_data:
            logger.info(row)