# src/controllers/cards_tab_controller.py
from .base_controller import BaseController

class CardsTabController(BaseController):
    def __init__(self, repository_factory):
        super().__init__(repository_factory)
        self.card_repository = self.repository_factory.create_card_repository()

    def get_card_repository(self):
        return self.card_repository

    def refresh_data(self):
        # Implement refresh logic for card data
        self.card_repository.refresh()  # Assuming this method exists in the repository
