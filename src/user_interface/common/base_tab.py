from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal
from configs.ui_settings import UISettings

class BaseTab(QWidget):
    update_status_signal = pyqtSignal(str, int)

    def __init__(self, logger, title):
        super().__init__()
        self.logger = logger
        self.title = title
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title_label = QLabel(self.title)
        title_label.setStyleSheet(UISettings.TITLE_LABEL_STYLE)
        layout.addWidget(title_label)

    def emit_status_update(self, message, timeout):
        self.update_status_signal.emit(message, timeout)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)