# src/utils/custom_logging/handlers.py
import logging
import logging.config
from .constants import DETAILED_LOG_FORMAT, SIMPLE_LOG_FORMAT
from rich.console import Console
from rich.theme import Theme

class RingBuffer(logging.StreamHandler):
    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.capacity = capacity
        self.buffer = []
        self.detailed_formatter = logging.Formatter(DETAILED_LOG_FORMAT)
        self.simple_formatter = logging.Formatter(SIMPLE_LOG_FORMAT)

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno <= logging.DEBUG:
            msg = self.detailed_formatter.format(record)
        else:
            msg = self.simple_formatter.format(record)
        self.buffer.append(msg)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def get(self) -> list[str]:
        return self.buffer

class DetailedRichHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)
        self.console = Console(
            log_time=True,
            log_time_format='%H:%M:%S-%f',
            theme=Theme(
                {
                    "traceback.border": "black",
                    "traceback.border.syntax_error": "black",
                    "inspect.value.border": "black",
                }
            ),
        )
        self.detailed_formatter = logging.Formatter(DETAILED_LOG_FORMAT)
        self.simple_formatter = logging.Formatter(SIMPLE_LOG_FORMAT)

    def emit(self, record):
        try:
            if record.levelno <= logging.DEBUG:
                message = self.detailed_formatter.format(record)
            else:
                message = self.simple_formatter.format(record)
            self.console.print(message, highlight=True)
        except Exception:
            self.handleError(record)
