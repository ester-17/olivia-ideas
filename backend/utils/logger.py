import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def setup_logger() -> logging.Logger:
    """Configure and return the application logger.
    
    The logger writes DEBUG-level messages and above to a rotating file
    and INFO-level messages and above to the console."""

    logger = logging.getLogger("olivia")
    logger.setLevel(logging.DEBUG)

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)
        

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s"
    )

    # Logs rotation: max 5MB, keeping up to 3 backups
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevents external library logs from cluttering the output
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("streamlit").setLevel(logging.WARNING)

    return logger
