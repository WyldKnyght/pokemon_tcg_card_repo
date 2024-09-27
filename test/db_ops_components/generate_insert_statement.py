# src/db_ops_components/generate_insert_statement.py
from .parse_schema import parse_schema
from config import Config

def generate_insert_statement(table_name, columns):
    placeholders = ', '.join(['?' for _ in columns])
    return f"INSERT OR REPLACE INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

schema = parse_schema(Config.SCHEMA_PATH)
for table, columns in schema.items():
    insert_statement = generate_insert_statement(table, columns)
    # Use this insert_statement in your insert functions