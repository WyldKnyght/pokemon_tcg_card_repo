Here's a brief overview of your new structure:

1. `__init__.py`: Serves as the entry point, importing and exposing the main components of your custom logging system.
2. `constants.py`: Contains all the constants and format strings used across the logging system.
3. `handlers.py`: Defines custom logging handlers (RingBuffer and DetailedRichHandler).
4. `setup_logging.py`: Contains the main setup_logging function to configure the logging system.
5. `decorators.py`: Includes utility decorators and context managers for error handling and temporary log level changes.
