# src/data_access/repositories/card_repository.py
from .base_repository import BaseRepository
from typing import List, Optional, Tuple

class CardRepository(BaseRepository):
    def get_columns(self) -> List[str]:
        query = "PRAGMA table_info(cards)"
        results = self.fetch_all(query)
        return [row[1] for row in results]  # Column name is at index 1

    def get_total_count(self) -> int:
        query = "SELECT COUNT(*) FROM cards"
        result = self.fetch_one(query)
        return result[0] if result else 0

    def get_page(self, offset: int, limit: int) -> List[Tuple]:
        query = "SELECT * FROM cards LIMIT ? OFFSET ?"
        return self.fetch_all(query, (limit, offset))

    def get_by_id(self, card_id: str) -> Optional[dict]:
        query = "SELECT * FROM cards WHERE id = ?"
        result = self.fetch_one(query, (card_id,))
        return dict(zip(self.get_columns(), result)) if result else None

    def get_by_set(self, set_id: str) -> List[dict]:
        query = "SELECT * FROM cards WHERE set_id = ?"
        results = self.fetch_all(query, (set_id,))
        columns = self.get_columns()
        return [dict(zip(columns, row)) for row in results]

    def search_by_name(self, name: str) -> List[dict]:
        query = "SELECT * FROM cards WHERE name LIKE ?"
        results = self.fetch_all(query, (f'%{name}%',))
        columns = self.get_columns()
        return [dict(zip(columns, row)) for row in results]
