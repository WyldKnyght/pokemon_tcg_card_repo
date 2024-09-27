# src/db_ops_components/load_card_data.py
import os
from tqdm import tqdm
from config import Config
from utils.custom_logging import logger
from db_ops_components.process_card_file import process_card_file

def load_card_data(cursor, schema):
    logger.info("Loading card data...")
    test_files = [Config.SET_ID_TO_FILENAME[set_id] for set_id in Config.TEST_SETS]
    with tqdm(total=len(test_files), desc="Processing card files") as pbar:
        for filename in test_files:
            file_path = os.path.join(Config.CARDS_DATA_DIR, filename)
            if os.path.exists(file_path):
                process_card_file(cursor, file_path, schema)
            else:
                logger.warning(f"File not found: {file_path}")
            pbar.update(1)