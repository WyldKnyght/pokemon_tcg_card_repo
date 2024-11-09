# src/user_interface/tab_widgets/admin_tab_widget.py
from PyQt6.QtWidgets import QPushButton, QMessageBox
from ..common.base_tab_widget import BaseTabWidget
from controllers.admin_tab_controller import AdminTabController
from configs.ui_settings import UISettings

class AdminTabWidget(BaseTabWidget):
    def setup(self):
        self.controller = AdminTabController(self.logger, self.repository_factory)

    def init_ui(self):
        self.check_updates_button = QPushButton(UISettings.ADMIN_CHECK_UPDATES_BUTTON_TEXT)
        self.check_updates_button.clicked.connect(self.check_for_updates)
        self.layout.addWidget(self.check_updates_button)

        self.update_repo_button = QPushButton(UISettings.ADMIN_UPDATE_REPO_BUTTON_TEXT)
        self.update_repo_button.clicked.connect(self.update_repo)
        self.layout.addWidget(self.update_repo_button)

    def check_for_updates(self):
        self.emit_status_update(UISettings.ADMIN_UPDATE_CHECK_START_MESSAGE, 
                                UISettings.ADMIN_UPDATE_CHECK_START_TIMEOUT)

        try:
            if self.controller.check_for_updates():
                QMessageBox.information(self, UISettings.ADMIN_UPDATE_SUCCESS_TITLE, 
                                        UISettings.ADMIN_UPDATE_SUCCESS_MESSAGE)
                self.log_info(UISettings.ADMIN_UPDATE_SUCCESS_MESSAGE)
                self.refresh_data_signal.emit()
            else:
                QMessageBox.information(self, UISettings.ADMIN_UPDATE_NO_CHANGES_TITLE, 
                                        UISettings.ADMIN_UPDATE_NO_CHANGES_MESSAGE)
                self.log_info(UISettings.ADMIN_UPDATE_NO_CHANGES_MESSAGE)
        except Exception as e:
            error_message = UISettings.ADMIN_UPDATE_ERROR_MESSAGE.format(str(e))
            QMessageBox.critical(self, UISettings.ADMIN_UPDATE_ERROR_TITLE, error_message)
            self.log_error(error_message)
        finally:
            self.emit_status_update(UISettings.ADMIN_UPDATE_CHECK_COMPLETE_MESSAGE, 
                                    UISettings.ADMIN_UPDATE_CHECK_COMPLETE_TIMEOUT)

    def update_repo(self):
        self.emit_status_update(UISettings.ADMIN_REPO_UPDATE_START_MESSAGE, 
                                UISettings.ADMIN_REPO_UPDATE_START_TIMEOUT)

        try:
            if self.controller.update_repo():
                QMessageBox.information(self, UISettings.ADMIN_REPO_UPDATE_SUCCESS_TITLE, 
                                        UISettings.ADMIN_REPO_UPDATE_SUCCESS_MESSAGE)
                self.log_info(UISettings.ADMIN_REPO_UPDATE_SUCCESS_MESSAGE)
            else:
                QMessageBox.information(self, UISettings.ADMIN_REPO_UPDATE_NO_CHANGES_TITLE, 
                                        UISettings.ADMIN_REPO_UPDATE_NO_CHANGES_MESSAGE)
                self.log_info(UISettings.ADMIN_REPO_UPDATE_NO_CHANGES_MESSAGE)
        except Exception as e:
            error_message = UISettings.ADMIN_REPO_UPDATE_ERROR_MESSAGE.format(str(e))
            QMessageBox.critical(self, UISettings.ADMIN_REPO_UPDATE_ERROR_TITLE, error_message)
            self.log_error(error_message)
        finally:
            self.emit_status_update(UISettings.ADMIN_REPO_UPDATE_COMPLETE_MESSAGE, 
                                    UISettings.ADMIN_REPO_UPDATE_COMPLETE_TIMEOUT)

    def refresh_data(self):
        # Implement if there's any data to refresh in the admin tab
        pass