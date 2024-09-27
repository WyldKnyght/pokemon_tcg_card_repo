# src/utils/create_db_tables.py
import os
import msvcrt
import sqlite3
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Get the current file's directory
current_file_path = Path(__file__).resolve()

# Define a function to find the root directory
def find_root_directory(start_path, marker):
    return next(
        (path for path in start_path.parents if (path / marker).exists()), None
    )

# Find the root directory using a marker (e.g., '.env' file)
root_dir = find_root_directory(current_file_path, '.env')

if root_dir is None:
    raise FileNotFoundError("Root directory not found. Ensure the marker file exists.")

# Resolve the full database and schema file paths from .env
db_path = root_dir / os.getenv("DB_PATH")
schema_file_path = root_dir / os.getenv("SCHEMA_PATH")

# Debugging output to verify paths
print(f"Current working directory: {Path.cwd()}")
print(f"Resolved database path: {db_path}")
print(f"Resolved schema file path: {schema_file_path}")

# Check if schema file exists
if not schema_file_path.exists():
    print(f"Schema file does not exist at: {schema_file_path}")
    exit(1)

# Ensure the directory for the database exists
db_path.parent.mkdir(parents=True, exist_ok=True)

def get_input_with_cancel(prompt):
    print(prompt, end='', flush=True)
    user_input = []
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b'\x1b':  # Esc key
                print("\nOperation canceled by the user.")
                exit()
            elif char in {b'\r', b'\n'}:  # Enter key
                print()  # Move to the next line
                return ''.join(user_input)
            else:
                user_input.append(char.decode())
                print(char.decode(), end='', flush=True)

def close_connection_if_open(conn):
    if conn:
        conn.close()

def remove_existing_database(db_path):
    db_path.unlink()
    if not db_path.exists():
        print(f"Existing database '{db_path}' has been removed successfully.")
    else:
        print(f"Failed to remove the database '{db_path}'. Check file permissions.")
        exit()

def handle_database_overwrite(db_path):
    remove_existing_database(db_path)

def handle_database_rename(db_path):
    while True:
        new_db_name = get_input_with_cancel("Enter a new name for the database file (without extension, e.g., 'inventory_v2'): ").strip()
        if not new_db_name.endswith('.db'):
            new_db_name += '.db'
        new_db_path = db_path.parent / new_db_name

        if not new_db_path.exists():
            return new_db_path
        response = get_input_with_cancel(f"The file '{new_db_path}' already exists. Try another name (y) or cancel (c)? ").strip().lower()
        if response == 'c':
            exit()

def handle_existing_database(db_path):
    if db_path.exists():
        response = get_input_with_cancel(f"The database file '{db_path}' already exists. Do you want to overwrite it (o), rename it (r), or cancel (c)? ").strip().lower()

        if response == 'o':
            handle_database_overwrite(db_path)
        elif response == 'r':
            return handle_database_rename(db_path)
        elif response == 'c':
            exit()

    return db_path

# Handle if the database file already exists
db_path = handle_existing_database(db_path)

# Connect to the SQLite database (it will create the file if it doesn't exist)
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Read and execute the schema
    with schema_file_path.open('r') as schema_file:
        create_tables_sql = schema_file.read()

    cursor.executescript(create_tables_sql)
    conn.commit()

print(f"Database and tables created successfully at '{db_path}'.")
