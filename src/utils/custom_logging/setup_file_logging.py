"""
This module provides functions for setting up file logging.

The `setup_file_logging` function creates a ConditionalFileHandler that logs
to a file in the ".logs" directory. The file name includes a timestamp and the
log level is set to INFO. The formatter is set to include the timestamp,
filename, function name, log level, and log message.

The `get_update_logger` function returns a logger that logs to the console with
the same formatter as the file handler.

The `enable_file_logging` function enables file logging by setting the
`should_log_to_file` attribute of the ConditionalFileHandler to True.
"""

import os
import logging
from datetime import datetime
from .handlers import ConditionalFileHandler


def setup_file_logging() -> ConditionalFileHandler:
    """
    Set up file logging.

    Returns:
        A ConditionalFileHandler that logs to a file in the ".logs" directory.
    """
    # Create the log directory if it doesn't exist
    log_dir = ".\logs"
    os.makedirs(log_dir, exist_ok=True)

    # Create a timestamp for the log file name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'update_log_{timestamp}.log')

    # Create the file handler
    file_handler = ConditionalFileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Set the formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    return file_handler


def get_update_logger() -> logging.Logger:
    """
    Get the update logger.

    Returns:
        A logger that logs to the console with the same formatter as the file
        handler.
    """
    logger = logging.getLogger('update_logger')
    logger.setLevel(logging.INFO)

    # Only add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def enable_file_logging(file_handler: ConditionalFileHandler) -> None:
    """
    Enable file logging.

    Args:
        file_handler: The ConditionalFileHandler to enable file logging for.
    """
    file_handler.enable_file_logging()

