# src/utils/custom_logging/decorators.py
import logging
from typing import Any, Callable
import functools
from contextlib import contextmanager

logger: logging.Logger = logging.getLogger(__name__)

# Decorator function
def error_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator for handling exceptions and logging errors.

    Args:
        func: The function to be decorated.

    Returns:
        A decorated function that logs any exceptions and re-raises them.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Log the error with the function name and the original exception
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            # You can customize the error handling here, e.g., re-raise the exception
            raise
    return wrapper

@contextmanager
def temporary_log_level(logger: logging.Logger, level: int):
    """
    Temporarily change the log level of a logger.

    Args:
        logger: The logger object.
        level: The temporary log level.

    Yields:
        None
    """
    old_level: int = logger.level  # type: ignore[assignment]
    logger.setLevel(level)
    try:
        yield
    finally:
        logger.setLevel(old_level)

