# src/controllers/db_modules/data_inserter.py
import json
import sqlite3
from typing import Dict, Any, List
from configs.env_settings import EnvSettings
from utils.custom_logging import logger

class DataInserter:
    def __init__(self, cursor: sqlite3.Cursor, schema: Dict[str, List[str]]):
        self.cursor = cursor
        self.schema = schema

    def insert_card(self, card: Dict[str, Any]) -> None:
        """Insert a card into the database."""
        set_id = card['id'].split('-')[0]
        if EnvSettings.ALLOWED_SET_IDS and set_id not in EnvSettings.ALLOWED_SET_IDS:
            return  # Skip this card if it's not from an allowed set

        try:
            # First, insert the main card data
            self._insert_into_table('cards', self.schema['cards'], self._map_data('cards', self.schema['cards'], card))

            # Then insert related data
            self._insert_card_related_data(card)
        except Exception as e:
            logger.error(f"Error inserting card {card['id']}: {str(e)}")

    def insert_card_set(self, card_set: Dict[str, Any]) -> None:
        """Insert a card set into the database."""
        try:
            # First, insert the main card set data
            self._insert_into_table('card_sets', self.schema['card_sets'], self._map_data('card_sets', self.schema['card_sets'], card_set))

            # Then insert related data
            self._insert_card_set_related_data(card_set)
        except Exception as e:
            logger.error(f"Error inserting card set {card_set.get('id', 'Unknown')}: {str(e)}")

    def _is_card_set_related_table(self, table_name: str) -> bool:
        """Check if the table is related to card set data."""
        return table_name == 'card_sets' or table_name.startswith('set_')

    def _insert_list_data(self, table_name: str, card_id: str, data_list: List[str]) -> None:
        """Insert list data into a table."""
        for item in data_list:
            self._insert_into_table(table_name, ['card_id', table_name.split('_')[1][:-1]], [card_id, item])

    def _map_data(self, table_name: str, columns: List[str], data: Dict[str, Any]) -> List[Any]:
        """Map data to database columns."""
        if table_name not in self.schema:
            return [None] * len(columns)

        json_key = self._get_json_key(table_name)
        nested_data = data if json_key == data else data.get(json_key, {})
        return [self._get_column_value(table_name, col, nested_data, data) for col in columns]

    def _get_column_value(self, table_name: str, column: str, nested_data: Any, full_data: Dict[str, Any]) -> Any:
        """Get the value for a specific column in a table."""
        if table_name in {'cards', 'card_sets'}:
            if column == 'id':
                return full_data.get('id')  # Ensure we're getting the id from the full_data
            if column == 'set_id':
                return full_data.get('id', '').split('-')[0]

        if isinstance(nested_data, dict):
            return nested_data.get(column)
        if isinstance(nested_data, list):
            return json.dumps(nested_data)
        return nested_data

    def _get_json_key(self, table_name: str) -> str:
        """Get the JSON key based on the table name."""
        if table_name in {'cards', 'card_sets'}:
            return table_name
        return table_name.split('_', 2)[-1]  # Handles both 'card_' and 'card_set_' prefixes

    def _insert_into_table(self, table_name: str, columns: List[str], values: List[Any]) -> None:
        """Insert data into a specified table."""
        # Filter out None values and their corresponding columns
        filtered_columns = [col for col, val in zip(columns, values) if val is not None]
        filtered_values = [val for val in values if val is not None]

        if not filtered_columns:
            logger.warning(f"No valid data to insert into {table_name}")
            return

        placeholders = ', '.join(['?' for _ in filtered_columns])
        query = f'''
        INSERT OR REPLACE INTO {table_name} ({', '.join(filtered_columns)})
        VALUES ({placeholders})
        '''
        try:
            self.cursor.execute(query, filtered_values)
        except sqlite3.Error as e:
            logger.error(f"SQLite error inserting into {table_name}: {str(e)}")
            logger.error(f"Query: {query}")
            logger.error(f"Values: {filtered_values}")
            raise

    def _insert_card_related_data(self, card: Dict[str, Any]) -> None:
        """Insert all data related to a card into various tables."""
        for table_name, columns in self.schema.items():
            if self._is_card_related_table(table_name) and table_name != 'cards':
                if table_name == 'card_subtypes':
                    self._insert_list_data(table_name, card['id'], card.get('subtypes', []))
                elif table_name == 'card_types':
                    self._insert_list_data(table_name, card['id'], card.get('types', []))
                else:
                    values = self._map_data(table_name, columns, card)
                    if any(value is not None for value in values):
                        self._insert_into_table(table_name, columns, values)

    def _insert_card_set_related_data(self, card_set: Dict[str, Any]) -> None:
        """Insert all data related to a card set into various tables."""
        for table_name, columns in self.schema.items():
            if self._is_card_set_related_table(table_name) and table_name != 'card_sets':
                values = self._map_data(table_name, columns, card_set)
                if any(value is not None for value in values):
                    self._insert_into_table(table_name, columns, values)

    def _is_card_related_table(self, table_name: str) -> bool:
        """Check if the table is related to card data."""
        return table_name == 'cards' or table_name.startswith('card_')

