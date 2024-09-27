import sqlite3
import logging
import os

db_file = r"M:\dev_env\pokemon-tcg-tracker\data\pokemon_tcg.db"
output_file = r"M:\dev_env\pokemon-tcg-tracker\data\output_schema.sql"


def extract_schema_to_file(db_file, output_file):
    logging.info(f"Extracting schema from {db_file} to {output_file}")

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Get tables
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Get indexes
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index';")
        indexes = cursor.fetchall()

        # Get views
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='view';")
        views = cursor.fetchall()

        # Write to output file
        with open(output_file, 'w') as file:
            write_schema_to_file(file, tables, indexes, views)

        logging.info(f"Schema extracted successfully to {output_file}")

    except sqlite3.Error as e:
        logging.error(f"SQLite error occurred: {e}")
    except IOError as e:
        logging.error(f"I/O error occurred: {e}")
    finally:
        if conn:
            conn.close()


def write_schema_to_file(file, tables, indexes, views):
    # Write tables
    file.write("-- Tables\n\n")
    for name, sql in tables:
        if sql:
            file.write(f"{sql};\n\n")

    # Write indexes
    file.write("-- Indexes\n\n")
    for name, sql in indexes:
        if sql:
            file.write(f"{sql};\n\n")

    # Write views
    file.write("-- Views\n\n")
    for name, sql in views:
        if sql:
            file.write(f"{sql};\n\n")

def ensure_dir_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Check if input file exists
    if not os.path.exists(db_file):
        logging.error(f"Database file not found: {db_file}")
        exit(1)

    # Ensure output directory exists
    ensure_dir_exists(output_file)

    # Extract schema
    extract_schema_to_file(db_file, output_file)