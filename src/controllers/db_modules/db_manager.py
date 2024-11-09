# src/controllers/db_modules/db_manager.py

import os
import sqlite3
from datetime import datetime
from configs.env_settings import EnvSettings
from utils.custom_logging import logger, error_handler

class DatabaseManager:
    """
    Database manager class responsible for managing database connections, schema
    execution, and data initialization.

    Attributes:
        conn (sqlite3.Connection): Database connection.
        cursor (sqlite3.Cursor): Database cursor.
    """
    def __init__(self):
        """
        Initializes the database manager.
        """
        self.conn = None
        self.cursor = None
        self.connection()

    def connection(self):
        """
        Establishes a connection to the database if it does not already exist.

        Returns:
            sqlite3.Connection: The database connection.
        """
        if self.conn is None:
            self.conn = sqlite3.connect(EnvSettings.DB_PATH)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.conn.cursor()
        return self.conn

    def close(self):
        """
        Closes the database connection if it exists.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def initialize_database(self):
        """
        Initializes the database by creating it if it does not exist and
        setting up the database schema and data version.
        """
        try:
            if not os.path.exists(EnvSettings.DB_PATH):
                logger.info("Database does not exist. Creating and initializing...")
                self.connection()  # Ensure connection is established
                self.setup_database()
                logger.info("Database created and initialized successfully.")
            else:
                logger.info("Database already exists.")
                self.connection()  # Ensure connection is established for existing database
        except Exception as e:
            logger.error(f"Error initializing database: {e}", exc_info=True)
            raise
        finally:
            self.close()

    @error_handler
    def execute_schema(self):
        """
        Executes the database schema by reading the schema file and executing
        the individual statements.

        Raises:
            sqlite3.OperationalError: If an error occurs while executing the
                schema.
        """
        with open(EnvSettings.SCHEMA_PATH, 'r') as schema_file:
            schema_script = schema_file.read()

        statements = schema_script.split(';')

        for statement in statements:
            if statement := statement.strip():
                try:
                    self.cursor.execute(statement)
                except sqlite3.OperationalError as e:
                    if "already exists" not in str(e):
                        logger.error(f"Error executing schema statement: {e}")
                        raise

        logger.info("Schema execution completed.")

    def initialize_data_version(self):
        """
        Initializes the data version table by creating it if it does not exist
        and inserting the current timestamp.
        """
        current_time = datetime.now().isoformat()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_version (
            last_update TEXT
        )
        """)
        self.cursor.execute("DELETE FROM data_version")
        self.cursor.execute("INSERT INTO data_version (last_update) VALUES (?)", (current_time,))
        logger.info(f"Initialized data_version with timestamp: {current_time}")

    def setup_database(self):
        """
        Sets up the database by executing the schema and initializing the
        data version.
        """
        self.execute_schema()
        self.initialize_data_version()
        self.commit()  # Commit changes after setup

    def commit(self):
        """
        Commits the current transaction to the database.
        """
        if self.conn:
            self.conn.commit()

    def rollback(self):
        """
        Rolls back the current transaction to the database.
        """
        if self.conn:
            self.conn.rollback()

    def get_last_update_time(self):
        """
        Gets the last update time from the data version table.

        Returns:
            datetime: The last update time.
        """
        self.connection()  # Ensure connection exists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS data_version (last_update TEXT)")
        self.cursor.execute("SELECT last_update FROM data_version")
        result = self.cursor.fetchone()
        return datetime.fromisoformat(result[0]) if result else None

    def set_last_update_time(self, time):
        """
        Sets the last update time in the data version table.

        Args:
            time (datetime): The new last update time.
        """
        self.connection()  # Ensure connection exists
        self.cursor.execute("DELETE FROM data_version")
        self.cursor.execute("INSERT INTO data_version (last_update) VALUES (?)", (time.isoformat(),))
        self.commit()  # Commit the change
