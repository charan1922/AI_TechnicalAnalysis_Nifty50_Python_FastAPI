from pymongo import MongoClient, errors
from app.core.config import settings
from app.core.logger import logging

logger = logging.getLogger(__name__)  # __name__ is the module name


def get_database():
    try:
        client = MongoClient(settings.mongo_db_uri, serverSelectionTimeoutMS=5000)
        # Explicitly check connection
        client.admin.command("ping")
        db = client[settings.db_name]
        logger.info("Connected to MongoDB successfully.")
        return db
    except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError) as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        return None
