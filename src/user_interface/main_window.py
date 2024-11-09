# src/user_interface/main_window.py
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QStatusBar
from PyQt6.QtGui import QAction
from configs.ui_settings import UISettings
from .cards_tab import CardsTab
from .admin_tab import AdminTab
from controllers.db_modules.db_manager import DatabaseManager
from data_access.repository_factory import RepositoryFactory
from controllers.main_window_controller import MainWindowController

class MainWindow(QMainWindow):
    def __init__(self, db_manager: DatabaseManager, repository_factory: RepositoryFactory, logger):
        super().__init__()
        self.logger = logger
        self.db_manager = db_manager
        self.repository_factory = repository_factory
        self.controller = MainWindowController(self.logger)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(UISettings.WINDOW_TITLE)
        self.setGeometry(*UISettings.WINDOW_GEOMETRY)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        self.cards_tab = CardsTab(self.logger, self.repository_factory)
        self.tab_widget.addTab(self.cards_tab, UISettings.CARDS_TAB_TITLE)

        self.admin_tab = AdminTab(self.logger, self.repository_factory)
        self.tab_widget.addTab(self.admin_tab, UISettings.ADMIN_TAB_TITLE)

        self.cards_tab.cards_widget.update_status_signal.connect(self.update_status_bar)
        self.admin_tab.admin_widget.update_status_signal.connect(self.update_status_bar)
        self.admin_tab.admin_widget.refresh_data_signal.connect(self.refresh_all_tabs)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.create_menu_bar()

    def refresh_all_tabs(self):
        self.controller.refresh_all_tabs(self.cards_tab, self.admin_tab)

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')

        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def update_status_bar(self, message, timeout):
        self.status_bar.showMessage(message, timeout)

    def closeEvent(self, event):
        if self.controller.confirm_exit():
            event.accept()
            self.logger.info("Application closed by user")
        else:
            event.ignore()