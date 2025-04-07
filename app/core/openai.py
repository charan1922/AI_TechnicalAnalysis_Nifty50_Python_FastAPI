from openai import OpenAI
from app.core.config import settings
from app.core.logger import logging

logger = logging.getLogger(__name__)

try:
    client = OpenAI(
        api_key=settings.openai_api_key,
    )
    logger.info("OpenAI client initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize OpenAI client: %s", e)
    raise
