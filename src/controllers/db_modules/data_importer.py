# src/controllers/db_modules/data_importer.py
import json
import os
from configs.env_settings import EnvSettings
from utils.custom_logging import logger
from .data_inserter import DataInserter
from data_access.repository_factory import RepositoryFactory

class DataImporter:
    def __init__(self, db_manager, repository_factory: RepositoryFactory):
        self.db_manager = db_manager
        self.repository_factory = repository_factory
        self.schema = self.repository_factory.get_schema()
        self.inserter = DataInserter(db_manager.cursor, self.schema)

    def import_data(self):
        self.import_card_sets()
        self.import_cards()
        self.db_manager.commit()
        logger.info("New data imported successfully.")

    def import_card_sets(self):
        logger.info("Starting to import set data...")
        with open(EnvSettings.SETS_DATA_PATH, 'r', encoding='utf-8') as f:
            sets_data = json.load(f)
        for set_data in sets_data:
            if not EnvSettings.ALLOWED_SET_IDS or set_data['id'] in EnvSettings.ALLOWED_SET_IDS:
                try:
                    self.inserter.insert_card_set(set_data)
                except Exception as e:
                    logger.error(f"Error inserting card set {set_data.get('id', 'Unknown')}: {str(e)}")
        logger.info("Set data import completed.")

    def import_cards(self):
        logger.info("Starting to import card data...")
        cards_count = 0
        for filename in os.listdir(EnvSettings.CARDS_DATA_DIR):
            if filename.endswith('.json'):
                with open(os.path.join(EnvSettings.CARDS_DATA_DIR, filename), 'r', encoding='utf-8') as f:
                    cards_data = json.load(f)
                for card_data in cards_data:
                    self.inserter.insert_card(card_data)
                    cards_count += 1
        logger.info(f"Imported {cards_count} cards.")
