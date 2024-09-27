# src/db_ops_components/setup_database.py
from .execute_schema import execute_schema
from .execute_script_with_retry import execute_script_with_retry

def setup_database(cursor):
    pragmas = '''
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;
        PRAGMA cache_size = 1000000;
        PRAGMA locking_mode = EXCLUSIVE;
        PRAGMA temp_store = MEMORY;
    '''
    execute_script_with_retry(cursor, pragmas)
    execute_schema(cursor)