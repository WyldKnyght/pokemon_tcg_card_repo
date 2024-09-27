# src/db_ops_components/query_data.py

import sqlite3
from config import Config
from utils.custom_logging import logger, error_handler
from db_ops_components.execute_query import execute_query
from db_ops_components.check_card_data import check_card_data
from db_ops_components.check_set_data import check_set_data
from db_ops_components.check_table_counts import check_table_counts
from tqdm import tqdm

@error_handler
def validate_data():
    """Validate the database by querying sample data and checking table contents."""
    logger.info("Starting database validation...")

    with sqlite3.connect(Config.DB_PATH) as conn:
        cursor = conn.cursor()

        # Define the total number of steps
        total_steps = 11  # 5 for cards, 5 for sets, 1 for table counts

        with tqdm(total=total_steps, desc="Validating database") as pbar:
            # Check sample cards
            cards = execute_query(cursor, 'SELECT * FROM cards LIMIT 5')
            logger.info("Sample Cards:")
            for card in cards:
                logger.info(card)
                check_card_data(cursor, card[0])
                pbar.update(1)

            # Check sample card sets
            sets = execute_query(cursor, 'SELECT * FROM card_sets LIMIT 5')
            logger.info("Sample Card Sets:")
            for card_set in sets:
                logger.info(card_set)
                check_set_data(cursor, card_set[0])
                pbar.update(1)

            # Check table row counts
            check_table_counts(cursor)
            pbar.update(1)

    logger.info("Database validation completed.")