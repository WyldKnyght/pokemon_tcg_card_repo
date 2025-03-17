# src/controllers/base_controller.py

class BaseController:
    def __init__(self, repository_factory):
        self.repository_factory = repository_factory

    def refresh_data(self):
        # This method should be overridden by child classes if needed
        pass
