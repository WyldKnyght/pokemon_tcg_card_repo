# src/db_ops_components/check_table_counts.py

import sqlite3
from utils.custom_logging import logger, error_handler
from db_ops_components.execute_query import execute_query

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