# src/controllers/db_operations/schema_executor.py
import sqlite3
from configs.env_settings import EnvSettings
from utils.custom_logging import logger, error_handler

class SchemaExecutor:

    @error_handler
    def execute_schema(self):
        """
        Executes the database schema by reading the schema file and executing
        the individual statements.
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
