# src/controllers/db_modules/data_update_service.py
from .data_importer import DataImporter
from utils.custom_logging import setup_file_logging, enable_file_logging
from utils.get_mod_time import get_latest_modification_time
from configs.env_settings import EnvSettings
from datetime import datetime
from data_access.repository_factory import RepositoryFactory

class DataUpdateService:
    def __init__(self, logger, repository_factory: RepositoryFactory):
        self.logger = logger
        self.repository_factory = repository_factory
        self.db_manager = repository_factory.db_manager
        self.card_repository = repository_factory.create_card_repository()
        self.set_repository = repository_factory.create_set_repository()

    def check_for_updates(self):
        self.logger.info("Starting update check...")

        try:
            if self._check_and_import_data():
                return self.handle_successful_update()
            self.logger.info("Update check completed. Data is up to date.")
            return False
        except Exception as e:
            self.logger.error(f"Error during update check: {str(e)}", exc_info=True)
            raise

    def _check_and_import_data(self):
        last_update = self.db_manager.get_last_update_time()
        self.logger.debug(f"Last update time: {last_update}")

        if last_update is None:
            self.logger.warning("No previous update time found. Performing initial import.")
            self._import_data()
            self.db_manager.set_last_update_time(datetime.now())
            return True

        # Check if any card set files have been modified
        card_sets_modification_time = get_latest_modification_time(EnvSettings.SETS_DATA_DIR)
        self.logger.debug(f"Card sets modification time: {card_sets_modification_time}")

        # Check if any card files have been modified
        cards_modification_time = get_latest_modification_time(EnvSettings.CARDS_DATA_DIR)
        self.logger.debug(f"Cards modification time: {cards_modification_time}")

        if card_sets_modification_time == 0 and cards_modification_time == 0:
            self.logger.error("Both card sets and cards directories are inaccessible or empty.")
            return False

        latest_modification = max(card_sets_modification_time, cards_modification_time)
        latest_modification_time = datetime.fromtimestamp(latest_modification) if latest_modification > 0 else None

        if latest_modification_time is None:
            self.logger.error("Unable to determine latest modification time.")
            return False

        if latest_modification_time > last_update:
            self.logger.info("New data detected. Starting import process...")
            self._import_data()
            self.db_manager.set_last_update_time(latest_modification_time)
            return True

        return False

    def _import_data(self):
        self.logger.debug("Starting data import process...")
        importer = DataImporter(self.db_manager, self.repository_factory)
        importer.import_data()
        self.logger.debug("Data import process completed.")

    def handle_successful_update(self):
        file_handler = setup_file_logging()
        enable_file_logging(file_handler)
        self.logger.addHandler(file_handler)
        self.logger.info("Update check completed. New data imported and view refreshed.")
        self.logger.removeHandler(file_handler)
        return True