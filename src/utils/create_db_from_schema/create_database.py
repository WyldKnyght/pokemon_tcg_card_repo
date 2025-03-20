
import sqlite3
from pathlib import Path
from .validate_schema import validate_schema
from ..custom_logging import logger, error_handler


@error_handler
def create_database(db_path: Path, schema_path: Path):
    """
    Create a SQLite database using the provided schema, ensuring that existing files are not overwritten.

    Args:
        db_path (Path): The path where the database file will be created.
        schema_path (Path): The path to the SQL schema file.
    """
    logger.info(f"Creating database at {db_path}")

    try:
        # Ensure the directory for the database exists
        logger.info(f"Ensuring database directory exists: {db_path.parent}")
        db_path.parent.mkdir(parents=True, exist_ok=True)

        # Check if the database file already exists
        if db_path.exists():
            logger.warning(f"Database file already exists at {db_path}. Skipping creation to avoid overwriting.")
            return  # Skip creation to prevent data loss

        # Check if schema file exists
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_path}")

        logger.info(f"Schema file found: {schema_path}")

        # Connect to the SQLite database (or create it if it doesn't exist)
        logger.info(f"Connecting to database: {db_path}")
        with sqlite3.connect(db_path) as conn:
            logger.info("Reading schema file...")
            with open(schema_path, 'r') as schema_file:
                schema = schema_file.read()
            logger.info("Executing schema...")
            conn.executescript(schema)
            logger.info("Schema executed.")

            # Verify database creation by checking tables
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            if tables := cursor.fetchall():
                logger.info(f"Database created successfully at {db_path}")
                logger.info(f"Tables created: {', '.join(table[0] for table in tables)}")
            else:
                logger.warning("Database created, but no tables found. Check your schema.")

        # Validate schema if applicable
        validate_schema(conn, schema)
    except sqlite3.Error as e:
        logger.error(f"An error occurred while creating the database: {e}")
    except FileNotFoundError as e:
        logger.error(str(e))

