import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.database import Database
from pymongo.errors import PyMongoError
from app.core.database import get_database
from app.core.logger import logging
from app.core.openai import client
from app.schemas.base import CamelCaseModel

# Initialize logger and router
logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/thread", tags=["threads"]
)  # tags=["threads"] is optional but recommended for OpenAPI docs grouping  (Swagger UI)
THREADS_COLLECTION = "threads"


class Thread(CamelCaseModel):
    thread_id: str
    analysis_name: str  # Name of the analysis
    created_at: datetime.datetime  # Timestamp for thread creation

    class Config:
        json_encoders = {
            datetime.datetime: lambda v: v.isoformat()  # Consistent datetime serialization
        }


class ThreadMessage(CamelCaseModel):
    run_id: Optional[str] = None  # Optional run_id with default None
    msg_id: str
    role: str
    thread_id: str
    message_text: str


class ThreadMessagesResponse(CamelCaseModel):
    messages: List[ThreadMessage]


# Endpoint to create a new thread (sync)
@router.get("/new", response_model=Thread, status_code=status.HTTP_201_CREATED)
def create_thread(name: str, db: Database = Depends(get_database)):
    """
    Creates a new thread using the OpenAI client and stores it in the database.

    Args:
        name (str): The name of the analysis for the thread (query parameter).
        db (Database): MongoDB database instance (injected via Depends).

    Returns:
        Thread: The created thread data.

    Raises:
        HTTPException: If OpenAI or database operations fail.
    """
    logger.info(f"Creating a new thread for analysis: {name}")

    # Validate name length (optional, remove if not needed)
    if not name.strip():
        logger.warning("Empty name provided for thread creation.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Name cannot be empty."
        )

    try:
        # Call OpenAI client synchronously
        thread = client.beta.threads.create()
        logger.debug(f"Thread created successfully with ID: {thread.id}")
    except Exception as e:
        logger.error(f"OpenAI thread creation failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to create thread with OpenAI service.",
        )

    # Prepare thread data
    thread_data = Thread(
        thread_id=thread.id,
        analysis_name=name,
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )

    try:
        # Save thread data synchronously
        result = db[THREADS_COLLECTION].insert_one(thread_data.model_dump())
        if not result.inserted_id:
            logger.error(f"Failed to insert thread {thread.id} into database.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save thread to database.",
            )
        logger.info(f"Thread {thread.id} saved to database successfully.")
        return thread_data
    except PyMongoError as e:
        logger.error(
            f"Database insertion failed for thread {thread.id}: {str(e)}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed.",
        )


# Endpoint to fetch all threads (sync)
@router.get("/allThreads", response_model=List[Thread])
def get_all_threads(db: Database = Depends(get_database)):
    """
    Retrieves all threads from the database.

    Args:
        db (Database): MongoDB database instance (injected via Depends).

    Returns:
        List[Thread]: List of all threads.

    Raises:
        HTTPException: If database retrieval fails.
    """
    logger.info("Retrieving all threads from the database.")

    try:
        threads_cursor = (
            db[THREADS_COLLECTION].find().sort("created_at", -1)
        )  # Sort newest first
        threads = [Thread(**thread) for thread in threads_cursor]  # Sync iteration
        logger.info(f"Retrieved {len(threads)} threads successfully.")
        return threads
    except PyMongoError as e:
        logger.error(f"Failed to retrieve threads: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve threads from database.",
        )


# Endpoint to fetch thread messages (sync)
@router.get("/{thread_id}/messages", response_model=ThreadMessagesResponse)
def thread_messages(thread_id: str):
    """
    Retrieves all messages for a given thread ID from OpenAI.

    Args:
        thread_id (str): The ID of the thread to fetch messages for.

    Returns:
        ThreadMessagesResponse: List of messages wrapped in a response model.

    Raises:
        HTTPException: If message retrieval fails.
    """
    logger.info(f"Retrieving messages for thread: {thread_id}")

    try:
        message_list = client.beta.threads.messages.list(
            thread_id=thread_id
        )  # Sync call
        messages = [
            ThreadMessage(
                run_id=message.run_id or None,
                msg_id=message.id,
                role=message.role,
                thread_id=message.thread_id,
                message_text=message.content[0].text.value if message.content else "",
            )
            for message in message_list
        ]
        messages.reverse()  # Reverse the order of messages
        logger.info(f"Retrieved {len(messages)} messages for thread {thread_id}.")
        return ThreadMessagesResponse(messages=messages)
    except Exception as e:
        logger.error(
            f"Failed to retrieve messages for thread {thread_id}: {str(e)}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to retrieve messages from OpenAI service.",
        )
