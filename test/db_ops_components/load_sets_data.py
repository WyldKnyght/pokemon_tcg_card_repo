# src/db_ops_components/load_sets_data.py
import json
from config import Config
from utils.custom_logging import logger
from .insert_set_data_batch import insert_set_data_batch


def load_sets_data(cursor, schema):
    logger.info("Loading set data...")
    with open(Config.SETS_DATA_PATH) as f:
        sets = json.load(f)
        test_sets = [card_set for card_set in sets if card_set['id'] in Config.TEST_SETS]
        insert_set_data_batch(cursor, test_sets, schema)