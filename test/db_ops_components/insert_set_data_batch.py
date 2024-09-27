# src/db_ops_components/insert_set_data_batch.py
import sqlite3
from typing import List, Dict, Any
from .generate_insert_statement import generate_insert_statement

def insert_set_data_batch(cursor: sqlite3.Cursor, card_sets: List[Dict[str, Any]], schema: Dict[str, List[str]]) -> None:
    for table, columns in schema.items():
        if table.startswith('set_') or table == 'card_sets':
            insert_statement = generate_insert_statement(table, columns)
            data = [
                [card_set.get(col, '') for col in columns]
                for card_set in card_sets
            ]
            cursor.executemany(insert_statement, data)