# src/controllers/db_modules/db_manager.py
import os
from typing import Optional
from datetime import datetime
from configs.env_settings import EnvSettings
from utils.custom_logging import logger
from .db_operations.db_connection import DatabaseConnection
from .db_operations.schema_executor import SchemaExecutor

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.database_connection = DatabaseConnection()
        self.schema_executor = SchemaExecutor()

    def initialize_database(self) -> None:
        if not os.path.exists(EnvSettings.DB_PATH):
            logger.info("Database does not exist. Creating and initializing...")
            self._ensure_connection()
            self._setup_database()
            logger.info("Database created and initialized successfully.")
        else:
            logger.info("Database already exists.")
            self._ensure_connection()

    def _ensure_connection(self) -> None:
        self.connection()
        self.cursor = self.conn.cursor()

    def _setup_database(self) -> None:
        self.execute_schema()
        self.initialize_data_version()
        self.commit()

    def initialize_data_version(self) -> None:
        current_time = datetime.now().isoformat()
        self._execute_sql(
            "CREATE TABLE IF NOT EXISTS data_version (last_update TEXT)",
            "DELETE FROM data_version",
            "INSERT INTO data_version (last_update) VALUES (?)",
            (current_time,),
        )
        logger.info(f"Initialized data_version with timestamp: {current_time}")

    def execute_schema(self) -> None:
        self.schema_executor.execute()

    def commit(self) -> None:
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        if self.conn:
            self.conn.rollback()

    def get_last_update_time(self) -> Optional[datetime]:
        self._ensure_connection()
        self.cursor.execute("SELECT last_update FROM data_version")
        result = self.cursor.fetchone()
        return datetime.fromisoformat(result[0]) if result else None

    def set_last_update_time(self, time: datetime) -> None:
        self._ensure_connection()
        self._execute_sql(
            "DELETE FROM data_version",
            "INSERT INTO data_version (last_update) VALUES (?)",
            (time.isoformat(),)
        )
        self.commit()

    def _execute_sql(self, *sql_statements: str, params: tuple = ()) -> None:
        for statement in sql_statements:
            self.cursor.execute(statement, params)
