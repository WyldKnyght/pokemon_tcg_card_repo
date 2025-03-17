# src/controllers/db_modules/db_manager.py
import sqlite3
from configs.env_settings import EnvSettings

class DatabaseConnection:
    def __init__(self):
        """Initializes the database manager."""
        self.conn = None
        self.cursor = None
        self.connection()

    def connection(self):
        """Establishes a connection to the database"""
        if self.conn is None:
            self.conn = sqlite3.connect(EnvSettings.DB_PATH)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.conn.cursor()
        return self.conn

    def close(self):
        """Closes the database connection if it exists."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
