# src/controllers/admin_tab_controller.py
from .base_controller import BaseController
from controllers.db_modules.data_update_service import DataUpdateService
from controllers.github_repo.update_repo import update_forked_repo, update_local_repo
from configs.env_settings import EnvSettings

class AdminTabController(BaseController):
    def __init__(self, logger, repository_factory):
        super().__init__(repository_factory)
        self.logger = logger
        self.data_update_service = DataUpdateService(logger, repository_factory)

    def check_for_updates(self):
        return self.data_update_service.check_for_updates()

    def update_repo(self):
        # Update the forked repository
        fork_updated = update_forked_repo(EnvSettings.REPO_PATH, EnvSettings.GITHUB_MY_REPO, EnvSettings.GITHUB_TCG_REPO)
        if not fork_updated:
            self.logger.error("Failed to update forked repository.")
            return False

        # Update the local repository
        local_updated = update_local_repo(EnvSettings.REPO_PATH)
        if not local_updated:
            self.logger.error("Failed to update local repository.")
            return False

        self.logger.info("Repository update completed successfully.")
        return True
