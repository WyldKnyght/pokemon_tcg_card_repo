import sqlite3
from contextlib import contextmanager
from config import Config

class DatabasePool:
    def __init__(self, db_path, max_connections=5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections = []

    @contextmanager
    def get_connection(self):
        if self.connections:
            connection = self.connections.pop()
        else:
            connection = sqlite3.connect(self.db_path)
        try:
            yield connection
        finally:
            if len(self.connections) < self.max_connections:
                self.connections.append(connection)
            else:
                connection.close()

# Usage
db_pool = DatabasePool(Config.DB_PATH)

with db_pool.get_connection() as conn:
    cursor = conn.cursor()
    # Perform database operations