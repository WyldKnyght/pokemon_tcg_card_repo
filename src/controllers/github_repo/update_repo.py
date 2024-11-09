# src/controllers/github_repo/update_repo.py
import os
import subprocess
from configs.env_settings import EnvSettings
from utils.custom_logging import logger
from typing import List, Optional

def run_command(command: List[str], cwd: Optional[str] = None) -> Optional[str]:
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True, cwd=cwd)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e}")
        logger.error(f"Error output: {e.stderr}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error running command: {e}")
        return None

def update_forked_repo(local_path: str, fork_url: str, original_repo: str) -> bool:
    """Update the forked repository with changes from the original repository."""
    if not os.path.exists(local_path):
        logger.error(f"Local repository path does not exist: {local_path}")
        return False

    # Set up remotes
    run_command(["git", "remote", "set-url", "origin", fork_url], cwd=local_path)
    remotes = run_command(["git", "remote"], cwd=local_path)
    if "upstream" not in remotes:
        run_command(["git", "remote", "add", "upstream", original_repo], cwd=local_path)

    # Fetch from upstream
    if run_command(["git", "fetch", "upstream"], cwd=local_path) is None:
        return False

    # Merge changes from upstream
    if run_command(["git", "merge", "upstream/master"], cwd=local_path) is None:
        return False

    # Push changes to your fork
    if run_command(["git", "push", "origin", "master"], cwd=local_path) is None:
        return False

    logger.info("Forked repository updated successfully.")
    return True

def update_local_repo(local_path: str) -> bool:
    """Update the local repository with changes from the remote."""
    if not os.path.exists(local_path):
        logger.error(f"Local repository path does not exist: {local_path}")
        return False

    # Fetch the latest changes
    if run_command(["git", "fetch", "origin"], cwd=local_path) is None:
        return False

    # Check if we're behind the remote
    status = run_command(["git", "status", "-uno"], cwd=local_path)
    if status is None:
        return False

    if "Your branch is behind" in status:
        logger.info("Updates available. Pulling changes...")
        if run_command(["git", "pull", "origin", "master"], cwd=local_path) is None:
            return False
        logger.info("Local repository updated successfully.")
    else:
        logger.info("Local repository is up to date.")

    return True

def main() -> None:
    # Update the forked repository
    if update_forked_repo(EnvSettings.REPO_PATH, EnvSettings.GITHUB_MY_REPO, EnvSettings.GITHUB_TCG_REPO):
        logger.info("Forked repository updated successfully.")
    else:
        logger.error("Failed to update forked repository.")

    # Update the local repository
    if update_local_repo(EnvSettings.REPO_PATH):
        logger.info("Local repository updated successfully.")
    else:
        logger.error("Failed to update local repository.")

if __name__ == "__main__":
    main()