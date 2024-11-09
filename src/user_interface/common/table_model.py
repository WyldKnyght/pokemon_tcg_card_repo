# src/user_interface/common/table_model.py
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from data_access.repositories.card_repository import CardRepository
from configs.ui_settings import UISettings
from controllers.table_model_controller import TableModelController

class TableModel(QAbstractTableModel):
    def __init__(self, card_repository: CardRepository):
        super().__init__()
        self.card_repository = card_repository
        self.controller = TableModelController(card_repository, UISettings.TABLE_PAGE_SIZE)
        self.load_data()

    def load_data(self):
        self.controller.load_data()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.controller.get_data(index.row(), index.column())

    def rowCount(self, index):
        return self.controller.get_row_count()

    def columnCount(self, index):
        return self.controller.get_column_count()

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.controller.get_header_data(section)

    def canFetchMore(self, index):
        return self.controller.can_fetch_more()

    def fetchMore(self, index):
        if self.controller.can_fetch_more():
            self.beginInsertRows(QModelIndex(), self.rowCount(QModelIndex()), 
                                    self.rowCount(QModelIndex()) + self.controller.get_fetch_more_count() - 1)
            self.controller.fetch_more()
            self.endInsertRows()

    def refresh_data(self):
        self.beginResetModel()
        self.controller.refresh_data()
        self.endResetModel()