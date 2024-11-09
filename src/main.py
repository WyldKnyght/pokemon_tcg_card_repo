# src/main.py
import sys
from PyQt6.QtWidgets import QApplication
from user_interface.main_window import MainWindow
from controllers.db_modules.db_manager import DatabaseManager
from utils.custom_logging import get_update_logger
from data_access.repository_factory import RepositoryFactory

def setup_and_run_application(_logger):
    # Initialize the database if it doesn't exist
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    repository_factory = RepositoryFactory(db_manager)

    # Launch the GUI
    app = QApplication(sys.argv)
    window = MainWindow(db_manager, repository_factory, _logger)
    window.show()
    sys.exit(app.exec())

def main():
    logger = get_update_logger()

    try:
        setup_and_run_application(logger)
    except Exception as e:
        logger.error(f"Unhandled exception in main: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()