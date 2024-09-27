# src/controllers/insert_card.py
import json
import sqlite3
import os
import logging
from typing import Dict, Any, List
from config import Config

logger = logging.getLogger(__name__)

def parse_and_insert_cards(cursor: sqlite3.Cursor, cards_dir: str, schema: Dict[str, List[str]]) -> None:
    """Parse all card JSON files in the directory and insert data into the database."""
    for filename in os.listdir(cards_dir):
        if filename.endswith('.json'):
            set_id = filename.split('.')[0]  # Assuming filename format is 'setid.json'
            if not Config.ALLOWED_SET_IDS or set_id in Config.ALLOWED_SET_IDS:
                with open(os.path.join(cards_dir, filename), 'r', encoding='utf-8') as f:
                    cards_data = json.load(f)

                for card in cards_data:
                    insert_card(cursor, card, schema)

def insert_card(cursor: sqlite3.Cursor, card: Dict[str, Any], schema: Dict[str, List[str]]) -> None:
    """Insert a card into the database."""
    set_id = card['id'].split('-')[0]
    if Config.ALLOWED_SET_IDS and set_id not in Config.ALLOWED_SET_IDS:
        return  # Skip this card if it's not from an allowed set

    try:
        insert_card_data(schema, card, cursor)
    except Exception as e:
        logger.error(f"Error inserting card {card['id']}: {str(e)}")

def insert_card_data(schema: Dict[str, List[str]], card: Dict[str, Any], cursor: sqlite3.Cursor) -> None:
    """Insert all data related to a card into various tables."""
    insert_main_card_data(schema, card, cursor)
    insert_related_card_data(schema, card, cursor)
    logger.debug(f"Inserted card: {card['id']}")

def insert_main_card_data(schema: Dict[str, List[str]], card: Dict[str, Any], cursor: sqlite3.Cursor) -> None:
    """Insert data into the main 'cards' table."""
    if 'cards' in schema:
        values = [json_to_db_mapping('cards', col, card) for col in schema['cards']]
        if any(value is not None for value in values):
            insert_into_table(cursor, 'cards', schema['cards'], values)

def insert_related_card_data(schema: Dict[str, List[str]], card: Dict[str, Any], cursor: sqlite3.Cursor) -> None:
    """Insert data into related card tables."""
    for table_name, columns in schema.items():
        if table_name.startswith('card_'):
            insert_card_related_table(table_name, columns, card, cursor)

def insert_card_related_table(table_name: str, columns: List[str], card: Dict[str, Any], cursor: sqlite3.Cursor) -> None:
    """Insert data into a single related card table."""
    json_key = table_name[5:]  # Remove 'card_' prefix
    if json_key in card:
        data = card[json_key]
        if isinstance(data, list):
            insert_list_data(table_name, columns, card['id'], data, cursor)
        else:
            insert_single_data(table_name, columns, card['id'], data, cursor)

def insert_list_data(table_name: str, columns: List[str], card_id: str, data: List[Any], cursor: sqlite3.Cursor) -> None:
    """Insert list data into a table."""
    for item in data:
        insert_single_data(table_name, columns, card_id, item, cursor)

def insert_single_data(table_name: str, columns: List[str], card_id: str, data: Any, cursor: sqlite3.Cursor) -> None:
    """Insert dictionary or simple data into a table."""
    values = [card_id]
    for col in columns:
        if col != 'card_id':
            value = data.get(col) if isinstance(data, dict) else data
            if isinstance(value, list):
                value = json.dumps(value)  # Convert list to JSON string
            values.append(value)
    insert_into_table(cursor, table_name, columns, values)

def json_to_db_mapping(table_name: str, key: str, card: Dict[str, Any]) -> Any:
    """Map JSON data to database columns."""
    if table_name == 'card_images':
        return card.get('images', {}).get(key)
    elif table_name == 'card_legalities':
        return card.get('legalities', {}).get(key)
    elif table_name == 'cards':
        return card['id'].split('-')[0] if key == 'set_id' else card.get(key)
    else:
        return card.get(key)

def insert_into_table(cursor: sqlite3.Cursor, table_name: str, columns: List[str], values: List[Any]) -> None:
    """Insert data into a specified table."""
    placeholders = ', '.join(['?' for _ in columns])
    query = f'''
    INSERT OR REPLACE INTO {table_name} ({', '.join(columns)})
    VALUES ({placeholders})
    '''
    try:
        cursor.execute(query, values)
    except sqlite3.Error as e:
        logger.error(f"SQLite error inserting into {table_name}: {str(e)}")
        raise