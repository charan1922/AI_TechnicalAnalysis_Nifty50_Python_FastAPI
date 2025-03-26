import datetime
from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from app.core.database import get_database
from app.core.logger import logging
from app.core.openai import client
from app.schemas.base import CamelCaseModel

# Initialize logger and router
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/threads", tags=["threads"])


# Define the Thread model using Pydantic
class Thread(CamelCaseModel):
    thread_id: str
    analysis_name: str  # Name of the analysis
    created_at: datetime.datetime  # Timestamp for thread creation


# Endpoint to create a new thread
@router.get("/new", response_model=Thread)
async def create_thread(name: str, db: Database = Depends(get_database)):
    """
    Creates a new thread using the OpenAI client and stores it in the database.

    Args:
        name (str): The name of the analysis for the thread.
        db (Database): MongoDB database instance (injected via Depends).

    Returns:
        Thread: The created thread data.
    """
    logger.info("Creating a new thread using OpenAI client.")

    try:
        # Call OpenAI client to create a thread
        thread = client.beta.threads.create()
    except Exception as e:
        logger.error(f"OpenAI thread creation failed: {e}")
        raise HTTPException(status_code=500, detail="OpenAI thread creation failed.")

    # Prepare thread data for insertion into the database
    thread_data = Thread(
        thread_id=thread.id,
        analysis_name=name,
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )

    # Save thread data in snake_case to the database
    result = db["threads"].insert_one(thread_data.model_dump())  # Save without aliases

    # Check if the insertion was successful
    if not result.inserted_id:
        logger.error("Failed to insert thread into database.")
        raise HTTPException(status_code=500, detail="Failed to create thread.")

    logger.info("Thread created successfully.")

    # Return thread data in camelCase to the client
    return thread_data  # Automatically uses aliases (camelCase) due to Pydantic Config
