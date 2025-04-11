from pymongo import MongoClient, errors
from app.core.config import settings
from app.core.logger import logging
import time

logger = logging.getLogger(__name__)


def get_database():
    """
    Connect to the MongoDB database.

    Returns:
        Database: The connected MongoDB database instance.
    """
    retries = 3
    delay = 2
    for attempt in range(retries):
        try:
            client = MongoClient(settings.mongo_db_uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            db = client[settings.db_name]
            logger.info("Connected to MongoDB successfully.")
            return db
        except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError) as e:
            logger.error(f"Attempt {attempt + 1} - Failed to connect to MongoDB: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise Exception("Failed to connect to MongoDB after multiple attempts.")
