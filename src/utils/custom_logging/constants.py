# src/utils/custom_logging/constants.py
"""
Constants and default configuration for custom logging.
"""

from typing import Dict, Any

# Constants for magic strings
LOG_ASCTIME: str = "asctime"
LOG_CREATED: str = "created"
LOG_LEVEL: str = "levelname"
LOG_NAME: str = "name"
LOG_MESSAGE: str = "message"

# Detailed logging format string (for debug level)
# This format string is used for logging at the DEBUG level. It includes the
# timestamp, logger name, log level, and log message.
DETAILED_LOG_FORMAT: str = (
    f'{{ "{LOG_ASCTIME}":"%({LOG_ASCTIME})s", "{LOG_CREATED}":%({LOG_CREATED})f, '
    f'"{LOG_LEVEL}":"%({LOG_LEVEL})s", "{LOG_NAME}":"%({LOG_NAME})s", '
    f'"{LOG_MESSAGE}":"%({LOG_MESSAGE})s" }}'
)

# Simple logging format string (for info level and above)
# This format string is used for logging at the INFO level and above. It only
# includes the timestamp, log level, and log message.
SIMPLE_LOG_FORMAT: str = f'%({LOG_ASCTIME})s - %({LOG_LEVEL})s - %({LOG_MESSAGE})s'

# Default logging configuration
# This dictionary contains the default configuration for custom logging. It
# includes the log level, ring buffer capacity, and detailed logging format.
DEFAULT_LOGGING_CONFIG: Dict[str, Any] = {
    'level': 'DEBUG',
    'ring_buffer_capacity': 100,
}

