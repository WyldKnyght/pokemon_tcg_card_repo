# src/db_operations.py

import sqlite3
import os
import json
from typing import List, Dict, Any
from config import Config
from utils.custom_logging import logger, error_handler
from db_ops_components import get_db_connection, execute_schema, insert_set_data_batch, insert_card_data_batch, check_tables

get_db_connection()
execute_schema()
insert_set_data_batch()
insert_card_data_batch()
check_tables()


@error_handler
def check_table_counts(cursor: sqlite3.Cursor) -> None:
    """Check row counts for all tables."""
    all_tables = [
        'cards', 'card_sets', 'card_subtypes', 'card_types',
        'card_evolves_to', 'card_rules', 'card_ancient_traits',
        'card_abilities', 'card_attacks', 'card_weaknesses',
        'card_resistances', 'card_retreat_cost',
        'card_national_pokedex_numbers', 'card_legalities',
        'card_images', 'card_tcgplayer', 'card_cardmarket',
        'set_legalities', 'set_images'
    ]

    for table in all_tables:
        count = execute_query(cursor, f'SELECT COUNT(*) FROM {table}')[0][0]
        logger.info(f"{table}: {count} rows")