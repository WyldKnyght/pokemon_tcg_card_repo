# src/configs/ui_settings.py

class UISettings:
    WINDOW_TITLE = "Pokemon TCG Card Repository"
    WINDOW_GEOMETRY = (100, 100, 1200, 800)
    CARDS_TAB_TITLE = "Pokemon Cards"
    ADMIN_TAB_TITLE = "Admin"
    EXIT_DIALOG_TITLE = "Exit"
    EXIT_DIALOG_MESSAGE = "Are you sure you want to exit?"
    TITLE_LABEL_STYLE = "font-size: 18px; font-weight: bold;"
    SEARCH_PLACEHOLDER = "Search cards..."
    REFRESH_BUTTON_TEXT = "Refresh"

    # Table model settings
    TABLE_PAGE_SIZE = 100

    # Admin tab settings
    ADMIN_UPDATE_CHECK_START_MESSAGE = "Checking for updates..."
    ADMIN_UPDATE_CHECK_START_TIMEOUT = 2000
    ADMIN_UPDATE_CHECK_COMPLETE_MESSAGE = "Update check completed."
    ADMIN_UPDATE_CHECK_COMPLETE_TIMEOUT = 5000
    ADMIN_UPDATE_SUCCESS_TITLE = "Update"
    ADMIN_UPDATE_SUCCESS_MESSAGE = "New data imported. View will be refreshed."
    ADMIN_UPDATE_NO_CHANGES_TITLE = "Update"
    ADMIN_UPDATE_NO_CHANGES_MESSAGE = "Data is up to date."
    ADMIN_UPDATE_ERROR_TITLE = "Error"
    ADMIN_UPDATE_ERROR_MESSAGE = "An error occurred during the update: {}"

    # Admin tab settings
    ADMIN_CHECK_UPDATES_BUTTON_TEXT = "Check for Updates"
    ADMIN_UPDATE_REPO_BUTTON_TEXT = "Update Repository"

    # Repository update settings
    ADMIN_REPO_UPDATE_START_MESSAGE = "Updating repository..."
    ADMIN_REPO_UPDATE_START_TIMEOUT = 2000
    ADMIN_REPO_UPDATE_COMPLETE_MESSAGE = "Repository update completed."
    ADMIN_REPO_UPDATE_COMPLETE_TIMEOUT = 5000
    ADMIN_REPO_UPDATE_SUCCESS_TITLE = "Repository Update"
    ADMIN_REPO_UPDATE_SUCCESS_MESSAGE = "Repository updated successfully."
    ADMIN_REPO_UPDATE_NO_CHANGES_TITLE = "Repository Update"
    ADMIN_REPO_UPDATE_NO_CHANGES_MESSAGE = "Repository is already up to date."
    ADMIN_REPO_UPDATE_ERROR_TITLE = "Error"
    ADMIN_REPO_UPDATE_ERROR_MESSAGE = "An error occurred during the repository update: {}"