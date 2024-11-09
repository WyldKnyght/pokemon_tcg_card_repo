# M:\dev_env\pokemon_tcg_card_repo\src\user_interface\admin_tab.py
from .common.base_tab import BaseTab
from .tab_widgets.admin_tab_widget import AdminTabWidget
from data_access.repository_factory import RepositoryFactory
from configs.ui_settings import UISettings

class AdminTab(BaseTab):
    def __init__(self, logger, repository_factory: RepositoryFactory):
        super().__init__(logger, UISettings.ADMIN_TAB_TITLE)
        self.repository_factory = repository_factory
        self.init_admin_ui()

    def init_admin_ui(self):
        self.admin_widget = AdminTabWidget(self.logger, self.repository_factory)
        self.layout().addWidget(self.admin_widget)
