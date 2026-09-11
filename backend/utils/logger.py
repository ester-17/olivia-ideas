"""Centralized logging configuration for the application."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
LOG_FILE = BASE_DIR / "logs" / "app.log"


def setup_logger() -> logging.Logger:
    """Configure and return the application logger.

    The configuration is idempotent, which is important because Streamlit
    reruns the application script after each interaction.

    Returns:
        The configured ``olivia`` application logger.
    """
    logger = logging.getLogger("olivia")
    if logger.handlers:
        return logger

    LOG_FILE.parent.mkdir(exist_ok=True)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s"
    )
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    for library_name in ("google", "streamlit", "urllib3"):
        logging.getLogger(library_name).setLevel(logging.WARNING)

    return logger
