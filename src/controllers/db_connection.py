import sqlite3
from config import Config

def connect_to_db() -> sqlite3.Connection:
    """Connect to the SQLite database."""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn