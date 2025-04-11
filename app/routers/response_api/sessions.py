# Refactored imports for better readability
from fastapi import APIRouter, HTTPException, Depends, status
from pymongo.database import Database
from pymongo.errors import PyMongoError
from app.core.database import get_database
from app.core.logger import logging
from app.schemas.base import CamelCaseModel
from typing import List
import datetime
from bson import ObjectId

# Initialize logger and router
logger = logging.getLogger(__name__)
router = APIRouter(prefix="/sessions", tags=["sessions"])

# Constants for collection names
SESSIONS_COLLECTION = "sessions"


# Session model
class Session(CamelCaseModel):
    session_id: str
    analysis_name: str
    created_at: datetime.datetime

    class Config:
        json_encoders = {datetime.datetime: lambda v: v.isoformat()}


# Endpoint to create a new session
@router.post("/new", response_model=Session, status_code=status.HTTP_201_CREATED)
def create_session(analysis_name: str, db: Database = Depends(get_database)):
    """
    Creates a new session and stores it in the database.

    Args:
        analysis_name (str): The name of the analysis for the session.
        db (Database): MongoDB database instance.

    Returns:
        Session: The created session data.
    """
    logger.info(f"Creating a new session for analysis: {analysis_name}")

    if not analysis_name.strip():
        logger.warning("Empty analysis name provided.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Analysis name cannot be empty.",
        )

    session_data = Session(
        session_id=str(ObjectId()),
        analysis_name=analysis_name,
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )

    try:
        result = db[SESSIONS_COLLECTION].insert_one(session_data.model_dump())
        if not result.inserted_id:
            logger.error("Failed to insert session into database.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save session to database.",
            )
        logger.info("Session saved successfully.")
        return session_data
    except PyMongoError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed.",
        )


# Endpoint to fetch all sessions
@router.get("/", response_model=List[Session])
def get_all_sessions(db: Database = Depends(get_database)):
    """
    Retrieves all sessions from the database.

    Args:
        db (Database): MongoDB database instance.

    Returns:
        List[Session]: List of all sessions.
    """
    logger.info("Fetching all sessions from the database.")

    try:
        sessions_cursor = db[SESSIONS_COLLECTION].find().sort("created_at", -1)
        sessions = [Session(**session) for session in sessions_cursor]
        logger.info(f"Retrieved {len(sessions)} sessions.")
        return sessions
    except PyMongoError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sessions.",
        )
