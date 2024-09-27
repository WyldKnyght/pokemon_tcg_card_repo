# src/controllers/insert_card_set.py
import json
import sqlite3
from typing import Dict, Any
from config import Config

def parse_and_insert_sets(cursor: sqlite3.Cursor, sets_file: str, schema: Dict[str, Any]) -> None:
    """Parse the sets JSON file and insert data into the database."""
    with open(sets_file, 'r', encoding='utf-8') as f:
        sets_data = json.load(f)

    for card_set in sets_data:
        if not Config.ALLOWED_SET_IDS or card_set['id'] in Config.ALLOWED_SET_IDS:
            insert_card_set(cursor, card_set, schema)

def insert_card_set(cursor: sqlite3.Cursor, card_set: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """Insert a card set into the database."""
    for table_name, table_schema in schema.items():
        if table_name.startswith('set_') or table_name == 'card_sets':
            columns = table_schema  # schema now contains a list of column names
            placeholders = ', '.join(['?' for _ in columns])
            
            # Create a mapping between JSON keys and database columns
            json_to_db_mapping = {
                'card_sets': lambda key: card_set.get(key),
                'set_legalities': lambda key: card_set['legalities'].get(key.split('_')[-1]) if key != 'set_id' else card_set['id'],
                'set_images': lambda key: card_set['images'].get(key) if key != 'set_id' else card_set['id']
            }
            
            values = [json_to_db_mapping[table_name](col) for col in columns]
            
            cursor.execute(f'''
            INSERT OR REPLACE INTO {table_name} ({', '.join(columns)})
            VALUES ({placeholders})
            ''', values)