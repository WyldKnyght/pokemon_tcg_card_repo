# src/controllers/main_window_controller.py
from PyQt6.QtWidgets import QMessageBox
from configs.ui_settings import UISettings

class MainWindowController:
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def refresh_all_tabs(cards_tab, admin_tab):
        cards_tab.refresh_data()
        admin_tab.refresh_data()

    @staticmethod
    def confirm_exit():
        reply = QMessageBox.question(None, UISettings.EXIT_DIALOG_TITLE, 
                                        UISettings.EXIT_DIALOG_MESSAGE,
                                        QMessageBox.StandardButton.Yes | 
                                        QMessageBox.StandardButton.No,
                                        QMessageBox.StandardButton.No)
        return reply == QMessageBox.StandardButton.Yes
