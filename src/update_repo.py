# src/update_repo.py
import os
import subprocess
from config import Config
from utils.custom_logging import logger
from typing import List, Optional

def run_command(command: List[str]) -> Optional[str]:
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error running command: {e}")
        return None

def update_repo(repo_path: str) -> bool:
    """Check for updates and pull changes if available."""
    os.chdir(repo_path)

    # Fetch the latest changes
    if run_command(["git", "fetch"]) is None:
        return False

    # Check if we're behind the remote
    status = run_command(["git", "status", "-uno"])
    if status is None:
        return False

    if "Your branch is behind" in status:
        logger.info("Updates available. Pulling changes...")
        if run_command(["git", "pull"]) is None:
            return False
        logger.info("Repository updated successfully.")
    else:
        logger.info("Repository is up to date.")

    return True

def main() -> None:
    if not os.path.exists(Config.REPO_PATH):  # Changed from repo_path to REPO_PATH
        logger.error(f"Repository path does not exist: {Config.REPO_PATH}")
        return

    if update_repo(Config.REPO_PATH):  # Changed from repo_path to REPO_PATH
        logger.info("Repository check completed successfully.")
    else:
        logger.error("Failed to update repository.")

if __name__ == "__main__":
    main()