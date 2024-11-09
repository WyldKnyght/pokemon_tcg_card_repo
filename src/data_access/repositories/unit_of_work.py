# src/data_access/repositories/unit_of_work.py
from controllers.db_modules.db_manager import DatabaseManager
from .card_repository import CardRepository
from .set_repository import SetRepository

class UnitOfWork:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.cards = CardRepository(db_manager)
        self.sets = SetRepository(db_manager)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.db_manager.commit()
        else:
            self.db_manager.rollback()