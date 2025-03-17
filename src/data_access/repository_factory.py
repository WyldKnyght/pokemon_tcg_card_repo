# src/data_access/repository_factory.py
from controllers.db_modules.db_manager import DatabaseManager
from .repositories.card_repository import CardRepository
from .repositories.set_repository import SetRepository
from controllers.db_modules.schema_parser import SchemaParser
from configs.env_settings import EnvSettings

class RepositoryFactory:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.schema = self._load_schema()

    def create_card_repository(self):
        return CardRepository(self.db_manager)

    def create_set_repository(self):
        return SetRepository(self.db_manager)

    def get_schema(self):
        return self.schema

    @staticmethod
    def _load_schema():
        return SchemaParser.parse_schema(EnvSettings.SCHEMA_PATH)
