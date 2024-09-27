# src/db_ops_components/insert_card_data_batch.py
import sqlite3
from typing import List, Dict, Any
from .bulk_insert import generate_insert_statement
from .prepare_row_data import prepare_row_data
from .execute_insert import execute_insert

def insert_card_data_batch(cursor: sqlite3.Cursor, cards: List[Dict[str, Any]], schema: Dict[str, List[str]]) -> None:
    for table, columns in schema.items():
        if not table.startswith('card_'):
            continue
        
        insert_statement = generate_insert_statement(table, columns)
        data = [prepare_row_data(card, columns) for card in cards]
        execute_insert(cursor, insert_statement, data, table)