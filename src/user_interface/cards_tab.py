# M:\dev_env\pokemon_tcg_card_repo\src\user_interface\cards_tab.py
from .common.base_tab import BaseTab
from .tab_widgets.cards_tab_widget import CardsTabWidget
from data_access.repository_factory import RepositoryFactory
from configs.ui_settings import UISettings

class CardsTab(BaseTab):
    def __init__(self, logger, repository_factory: RepositoryFactory):
        super().__init__(logger, UISettings.CARDS_TAB_TITLE)
        self.repository_factory = repository_factory
        self.init_cards_ui()

    def init_cards_ui(self):
        self.cards_widget = CardsTabWidget(self.logger, self.repository_factory)
        self.layout().addWidget(self.cards_widget)

    def refresh_data(self):
        self.cards_widget.refresh_data()
