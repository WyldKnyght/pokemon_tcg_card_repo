import time
import sqlite3

def execute_query_with_retry(cursor, query, params=None, max_attempts=10, delay=10):
    for attempt in range(max_attempts):
        try:
            return cursor.execute(query, params)
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e) and attempt < max_attempts - 1:
                time.sleep(delay)
            else:
                raise
