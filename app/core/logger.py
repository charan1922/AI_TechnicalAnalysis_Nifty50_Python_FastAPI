import logging
import sys

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,  # Set log level to INFO
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",  # Log format
        handlers=[
            logging.StreamHandler(sys.stdout),  # Log to console
            logging.FileHandler("app.log", mode="a"),  # Log to file
        ],
    )

    # Customize specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("pymongo").setLevel(logging.WARNING)