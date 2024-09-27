# src/main.py
from controllers.db_connection import connect_to_db
from controllers.db_operations import setup_database_and_import_data

def main():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        setup_database_and_import_data(cursor, conn)
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()