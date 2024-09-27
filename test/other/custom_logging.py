# src/utils/custom_logging.py
import logging
import logging.config
import os
from rich.console import Console
from rich.theme import Theme
from typing import Any, Dict, Optional, Callable
import functools
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()





