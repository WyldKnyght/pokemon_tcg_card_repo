# src/controllers/db_operations.py
from config import Config
from controllers.db_setup import setup_database
from controllers.insert_card_set import parse_and_insert_sets
from controllers.insert_card import parse_and_insert_cards
from controllers.parse_schema import parse_schema

def perform_database_setup_and_data_import(cursor, conn):
    # Set up the database schema
    setup_database(cursor)

    # Parse the schema
    schema = parse_schema(Config.SCHEMA_PATH)

    # Parse and insert sets
    parse_and_insert_sets(cursor, Config.SETS_DATA_PATH, schema)

    # Parse and insert cards
    parse_and_insert_cards(cursor, Config.CARDS_DATA_DIR, schema)

    conn.commit()
    print("Database setup and data import completed successfully.")

def setup_database_and_import_data(cursor, conn):
    try:
        perform_database_setup_and_data_import(cursor, conn)
    except Exception as e:
        conn.rollback()
        print(f"Error in setup_database_and_import_data: {e}")
        raise