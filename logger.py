"""Logging setup. Logs go to a rotating file so the console stays clean."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import LOG_FILE


def setup_logging(log_file: Path = LOG_FILE, level: int = logging.INFO) -> None:
    """Configure the 'srms' logger. Falls back silently if the file is not writable."""
    logger = logging.getLogger("srms")
    logger.setLevel(level)
    if logger.handlers:  # already configured
        return
    try:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    except OSError:
        logger.addHandler(logging.NullHandler())
        return
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s"))
    logger.addHandler(handler)
