import logging
import sys
from logging.handlers import RotatingFileHandler


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                "app.log", maxBytes=5 * 1024 * 1024, backupCount=3
            ),  # 5MB log file
        ],
    )

    logging.getLogger("pymongo").setLevel(logging.WARNING)
