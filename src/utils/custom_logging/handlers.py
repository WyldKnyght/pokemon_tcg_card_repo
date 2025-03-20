# src/utils/custom_logging/handlers.py
import logging
from .constants import DETAILED_LOG_FORMAT, SIMPLE_LOG_FORMAT
from rich.console import Console
from rich.theme import Theme


class RingBuffer(logging.StreamHandler):
    """
    A custom logging handler that stores log messages in a ring buffer.

    The ring buffer is a list of strings, where each string is a formatted log
    message. The buffer is initially empty and has a maximum capacity. When the
    buffer is full and a new log message is emitted, the oldest message is
    removed from the buffer and the new message is added.
    """

    def __init__(self, capacity: int) -> None:
        """
        Initialize the ring buffer handler.

        Args:
            capacity: The maximum number of log messages to store in the buffer.
        """
        super().__init__()
        self.capacity = capacity
        self.buffer = []
        self.detailed_formatter = logging.Formatter(DETAILED_LOG_FORMAT)
        self.simple_formatter = logging.Formatter(SIMPLE_LOG_FORMAT)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Handle a log record.

        If the log record has a level of DEBUG or lower, it is formatted using
        the detailed formatter. Otherwise, it is formatted using the simple
        formatter. The formatted message is then added to the ring buffer.

        If the buffer is full, the oldest message is removed from the buffer
        before adding the new message.
        """
        if record.levelno <= logging.DEBUG:
            msg = self.detailed_formatter.format(record)
        else:
            msg = self.simple_formatter.format(record)
        self.buffer.append(msg)
        if len(self.buffer) > self.capacity:
            self.buffer.pop(0)

    def get(self) -> list[str]:
        """
        Return the contents of the ring buffer.

        Returns:
            A list of strings, where each string is a formatted log message.
        """
        return self.buffer


class DetailedRichHandler(logging.Handler):
    """
    A custom logging handler that prints log messages to the console using
    Rich.
    """

    def __init__(self, level=logging.NOTSET):
        """
        Initialize the Rich handler.

        Args:
            level: The minimum log level to print to the console.
        """
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

    def emit(self, record: logging.LogRecord) -> None:
        """
        Handle a log record.

        If the log record has a level of DEBUG or lower, it is formatted using
        the detailed formatter. Otherwise, it is formatted using the simple
        formatter. The formatted message is then printed to the console using
        Rich.
        """
        try:
            if record.levelno <= logging.DEBUG:
                message = self.detailed_formatter.format(record)
            else:
                message = self.simple_formatter.format(record)
            self.console.print(message, highlight=True)
        except Exception:
            self.handleError(record)


class ConditionalFileHandler(logging.Handler):
    """
    A custom logging handler that logs to a file, but only if a condition is
    met.

    The condition is set using the `enable_file_logging` method. If the
    condition is met, the handler will log to the file specified in the
    constructor. Otherwise, the handler will buffer log records and not log
    them to a file.
    """

    def __init__(self, filename, mode='a', encoding=None):
        """
        Initialize the conditional file handler.

        Args:
            filename: The name of the file to log to.
            mode: The mode to open the file in. Defaults to 'a'.
            encoding: The encoding to use when writing to the file. Defaults to
                None.
        """
        super().__init__()
        self.filename = filename
        self.mode = mode
        self.encoding = encoding
        self.should_log_to_file = False
        self.buffer = []

    def emit(self, record):
        """
        Handle a log record.

        If the condition is met, the handler will log to the file specified in
        the constructor. Otherwise, the handler will buffer the log record.
        """
        if self.should_log_to_file:
            if not hasattr(self, 'file_handler'):
                self.file_handler = logging.FileHandler(self.filename, self.mode, self.encoding)
                self.file_handler.setFormatter(self.formatter)
                for buffered_record in self.buffer:
                    self.file_handler.emit(buffered_record)
                self.buffer = []
            self.file_handler.emit(record)
        else:
            self.buffer.append(record)

    def enable_file_logging(self):
        """
        Enable logging to a file.

        This method sets the condition to True, so that the handler will log to
        the file specified in the constructor.
        """
        self.should_log_to_file = True

