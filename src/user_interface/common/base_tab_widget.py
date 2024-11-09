# src/user_interface/common/base_tab_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from data_access.repository_factory import RepositoryFactory

class BaseTabWidget(QWidget):
    update_status_signal = pyqtSignal(str, int)
    refresh_data_signal = pyqtSignal()

    def __init__(self, logger, repository_factory: RepositoryFactory):
        super().__init__()
        self.logger = logger
        self.repository_factory = repository_factory
        self.layout = QVBoxLayout(self)  
        self.setup()
        self.init_ui()

    def setup(self):
        # This method should be overridden by child classes to set up any necessary attributes
        pass

    def init_ui(self):
        # This method should be overridden by child classes
        pass

    def refresh_data(self):
        # This method should be overridden by child classes
        pass

    def emit_status_update(self, message: str, timeout: int):
        self.update_status_signal.emit(message, timeout)

    def log_info(self, message: str):
        self.logger.info(message)

    def log_error(self, message: str):
        self.logger.error(message)