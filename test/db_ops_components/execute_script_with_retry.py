# src/db_ops_components/execute_script_with_retry.py
import time
import sqlite3

def execute_script_with_retry(cursor, script, max_attempts=5, delay=1):
    for attempt in range(max_attempts):
        try:
            cursor.executescript(script)
            return
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_attempts - 1:
                time.sleep(delay)
            else:
                raise