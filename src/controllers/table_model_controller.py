# src/controllers/table_model_controller.py
from .base_controller import BaseController

class TableModelController(BaseController):
    def __init__(self, card_repository, page_size):
        super().__init__(None)  # TableModelController doesn't need repository_factory
        self.card_repository = card_repository
        self.page_size = page_size
        self.current_page = 0
        self.total_rows = 0
        self.columns = []
        self.cache = []

    def load_data(self):
        self.columns = self.card_repository.get_columns()
        self.total_rows = self.card_repository.get_total_count()
        self.fetch_page(self.current_page)

    def fetch_page(self, page):
        offset = page * self.page_size
        new_cache = self.card_repository.get_page(offset, self.page_size)
        self.cache.extend(new_cache)

    def get_data(self, row, column):
        return self.cache[row][column]

    def get_row_count(self):
        return min(len(self.cache), self.total_rows)

    def get_column_count(self):
        return len(self.columns)

    def get_header_data(self, section):
        return self.columns[section]

    def can_fetch_more(self):
        return len(self.cache) < self.total_rows

    def get_fetch_more_count(self):
        remaining = self.total_rows - len(self.cache)
        return min(remaining, self.page_size)

    def fetch_more(self):
        self.current_page += 1
        self.fetch_page(self.current_page)

    def refresh_data(self):
        self.current_page = 0
        self.cache.clear()
        self.load_data()