# src/utils/custom_logging/__init__.py
from .setup_logging import setup_logging
from .decorators import error_handler, temporary_log_level

import logging

# Create a pre-configured logger
logger = logging.getLogger(__name__)

__all__ = ['setup_logging', 'error_handler', 'temporary_log_level', 'logger']