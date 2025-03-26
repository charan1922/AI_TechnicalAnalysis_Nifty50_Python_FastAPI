import datetime
from fastapi import APIRouter, HTTPException, Depends
from pymongo.database import Database
from app.core.database import get_database
from app.core.logger import logging
from app.core.openai import client
from app.schemas.base import CamelCaseModel
from typing import List

# Initialize logger and router
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/thread", tags=["threads"])


# Define the Thread model using Pydantic
class Thread(CamelCaseModel):
    thread_id: str
    analysis_name: str  # Name of the analysis
    created_at: datetime.datetime  # Timestamp for thread creation


class ThreadMessage(CamelCaseModel):
    run_id: str
    msg_id: str
    role: str
    thread_id: str
    message_text: str


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
        logger.info("Thread created successfully.")
    except Exception as e:
        logger.error(f"OpenAI thread creation failed: {e}")
        raise HTTPException(status_code=500, detail="OpenAI thread creation failed.")

    # Prepare thread data for insertion into the database
    thread_data = Thread(
        thread_id=thread.id,
        analysis_name=name,
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )

    try:
        # Save thread data in snake_case to the database
        result = db["threads"].insert_one(
            thread_data.model_dump()
        )  # Save without aliases

        # Check if the insertion was successful
        if not result.inserted_id:
            logger.error("Failed to insert thread into database.")
            raise HTTPException(status_code=500, detail="Failed to create thread.")

        logger.info("Thread saved to database successfully.")

        # Return thread data in camelCase to the client
        return thread_data

    except Exception as e:
        logger.error(f"Failed to insert thread into database: {e}")
        raise HTTPException(status_code=500, detail="Database insertion failed.")


@router.get("/allThreads", response_model=List[Thread])
async def get_all_threads(db: Database = Depends(get_database)):
    logger.info("Retrieving all threads from the database.")

    try:
        threads_cursor = db["threads"].find()
        threads = []
        for thread in threads_cursor:
            thread_obj = Thread(
                **thread
            )  # **thread unpacks the dictionary into keyword arguments
            threads.append(thread_obj)

        logger.info(f"{len(threads)} threads retrieved successfully.")
        return threads
    except Exception as e:
        logger.error(f"Failed to retrieve threads: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving threads."
        )


@router.get("/{thread_id}/messages", response_model=List[ThreadMessage])
async def thread_messages(thread_id: str):
    logger.info(f"Retrieving messages for thread: {thread_id}")

    try:
        messageList = client.beta.threads.messages.list(thread_id=thread_id)
        messages = []
        for message in messageList:
            message_obj = ThreadMessage(
                run_id=message.run_id or "",
                msg_id=message.id,
                role=message.role,
                thread_id=message.thread_id,
                message_text=message.content[0].text.value if message.content else "",
            )
            messages.append(message_obj)

        logger.info(f"{len(messages)} messages retrieved successfully.")
        return messages
    except Exception as e:
        logger.error(f"Failed to retrieve messages: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="An error occurred while retrieving messages."
        )
