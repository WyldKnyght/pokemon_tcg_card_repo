# src/utils/custom_logging/__init__.py
"""
This module provides functions and classes for custom logging configurations.

The `setup_logging` function configures the root logger to log to a file and
console with a custom format. The `error_handler` function is a decorator that
catches and logs exceptions. The `temporary_log_level` function is a context
manager that temporarily changes the log level of a logger.

The `get_update_logger` function returns a logger that logs to a file in the
`.logs` directory. The `enable_file_logging` function enables file logging for
the logger returned by `get_update_logger`. The `ConditionalFileHandler` class
is a custom file handler that logs to a file if the `should_log_to_file`
attribute is set to `True`.

The `logger` variable is a pre-configured logger that logs to the console with
the custom format.
"""

from .setup_logging import setup_logging
from .decorators import error_handler, temporary_log_level
from .setup_file_logging import get_update_logger, enable_file_logging, ConditionalFileHandler

import logging

# Create a pre-configured logger
logger: logging.Logger = logging.getLogger(__name__)

__all__: list[str] = [
    'setup_logging',
    'error_handler',
    'temporary_log_level',
    'logger',
    'get_update_logger',
    'enable_file_logging',
    'ConditionalFileHandler',
]

