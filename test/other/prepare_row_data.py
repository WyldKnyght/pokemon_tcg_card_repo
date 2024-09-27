# src/db_ops_components/prepare_row_data.py
from typing import List, Dict, Any

def prepare_row_data(card: Dict[str, Any], columns: List[str]) -> tuple:
    row = []
    for col in columns:
        value = card.get(col, '')
        if isinstance(value, list):
            value = ','.join(map(str, value))
        row.append(value)
    return tuple(row)