# src/data_access/repositories/set_repository.py
from .base_repository import BaseRepository
from typing import List, Optional

class SetRepository(BaseRepository):
    def get_by_id(self, set_id: str) -> Optional[dict]:
        query = "SELECT * FROM card_sets WHERE id = ?"
        result = self.fetch_one(query, (set_id,))
        return dict(zip([column[0] for column in self.db_manager.cursor.description], result)) if result else None

    def get_all(self) -> List[dict]:
        query = "SELECT * FROM card_sets"
        results = self.fetch_all(query)
        return [dict(zip([column[0] for column in self.db_manager.cursor.description], row)) for row in results]

    def search_by_name(self, name: str) -> List[dict]:
        query = "SELECT * FROM card_sets WHERE name LIKE ?"
        results = self.fetch_all(query, (f'%{name}%',))
        return [dict(zip([column[0] for column in self.db_manager.cursor.description], row)) for row in results]
