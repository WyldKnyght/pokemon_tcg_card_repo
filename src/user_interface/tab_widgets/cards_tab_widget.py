# src/user_interface/tab_widgets/cards_tab_widget.py
from PyQt6.QtWidgets import QTableView
from PyQt6.QtCore import QModelIndex
from ..common.base_tab_widget import BaseTabWidget
from ..common.table_model import TableModel
from controllers.cards_tab_controller import CardsTabController

class CardsTabWidget(BaseTabWidget):
    def setup(self):
        self.controller = CardsTabController(self.repository_factory)

    def init_ui(self):
        self.table = QTableView()
        self.model = TableModel(self.controller.get_card_repository())
        self.table.setModel(self.model)
        self.table.verticalScrollBar().valueChanged.connect(self.check_scroll)
        self.layout.addWidget(self.table)

    def check_scroll(self, value):
        if value == self.table.verticalScrollBar().maximum():
            self.model.fetchMore(QModelIndex())

    def refresh_data(self):
        self.model.refresh_data()