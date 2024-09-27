# src/db_ops_components/process_card_file.py
import os
import time
import sqlite3
import ijson
from utils.custom_logging import logger
from config import Config
from .data_insert import DataInsert
from tqdm import tqdm

def retry_on_db_lock(func):
    def wrapper(*args, **kwargs):
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e) and attempt < max_attempts - 1:
                    time.sleep(1)  # Wait for 1 second before retrying
                else:
                    raise
    return wrapper

def process_card_files(cursor, schema, file_paths, test_mode=True):
    for file_path in tqdm(file_paths, desc="Processing card files"):
        process_card_file(cursor, file_path, schema, test_mode)

@retry_on_db_lock
def process_card_file(cursor, file_path, schema, test_mode=True, chunk_size=1000):
    data_insert = DataInsert(cursor, schema)
    cards_processed = 0
    cards_inserted = 0

    try:
        with open(file_path, 'rb') as f:
            cards = []
            for card in ijson.items(f, 'item'):
                cards_processed += 1
                if test_mode and all(
                    set_id not in card.get('id', '')
                    for set_id in Config.TEST_SETS
                ):
                    continue
                cards.append(card)
                if len(cards) >= chunk_size:
                    data_insert.insert_card_data_batch(cards)
                    cards_inserted += len(cards)
                    cards = []

            if cards:
                data_insert.insert_card_data_batch(cards)
                cards_inserted += len(cards)

        logger.info(f"Processed {cards_processed} cards, inserted {cards_inserted} cards from {os.path.basename(file_path)}")
    except UnicodeDecodeError as e:
        logger.error(f"Error decoding {os.path.basename(file_path)}: {str(e)}")
    except ValueError as e:
        logger.error(f"Error parsing JSON in {os.path.basename(file_path)}: {str(e)}")

    return cards_processed, cards_inserted

def load_card_data(cursor, schema, test_mode=True):
    logger.info("Loading card data...")
    if test_mode:
        files = [Config.SET_ID_TO_FILENAME[set_id] for set_id in Config.TEST_SETS]
    else:
        files = os.listdir(Config.CARDS_DATA_DIR)
    
    file_paths = [os.path.join(Config.CARDS_DATA_DIR, filename) for filename in files]
    process_card_files(cursor, schema, file_paths, test_mode)