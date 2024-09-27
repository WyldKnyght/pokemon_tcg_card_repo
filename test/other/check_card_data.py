# src/db_ops_components/check_card_data.py
import sqlite3
from utils.custom_logging import logger, error_handler
from .execute_query import execute_query

@error_handler
def check_card_data(cursor: sqlite3.Cursor, card_id: str) -> None:
    """Check related tables for a specific card."""
    tables = [
        'card_subtypes', 'card_types', 'card_evolves_to',
        'card_rules', 'card_ancient_traits', 'card_abilities',
        'card_attacks', 'card_weaknesses',
        'card_resistances', 'card_retreat_cost',
        'card_national_pokedex_numbers',
        'card_legalities', 'card_images',
        'card_tcgplayer', 'card_cardmarket'
    ]

    for table in tables:
        related_data = execute_query(cursor, f'SELECT * FROM {table} WHERE card_id = ?', (card_id,))
        logger.info(f"{table} for card {card_id}:")
        for row in related_data:
            logger.info(row)
