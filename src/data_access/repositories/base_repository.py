# src/data_access/repositories/base_repository.py
from controllers.db_modules.db_manager import DatabaseManager

class BaseRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def execute(self, query: str, params: tuple = None):
        conn = self.db_manager.connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor

    def fetch_all(self, query: str, params: tuple = None):
        cursor = self.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query: str, params: tuple = None):
        cursor = self.execute(query, params)
        return cursor.fetchone()
