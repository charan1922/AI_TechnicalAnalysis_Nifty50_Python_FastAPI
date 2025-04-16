from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import StreamingResponse
from app.schemas.base import CamelCaseModel
from app.utils.function_handlers import handle_tool_outputs
from app.core.openai import client
from app.core.config import settings
from app.core.logger import logging
from typing import Dict, Any, List
from pydantic import BaseModel
import asyncio
from app.tools.tools import tools
import json
from app.core.database import get_database
from bson import ObjectId
from datetime import datetime, timezone
from pymongo.database import Database
from pymongo.errors import PyMongoError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/response", tags=["response"])

instructions = "You are designed to provide comprehensive technical analysis for the top 50 stocks in the Nifty index. You offer insights on various technical indicators to aid in making informed buying and selling decisions. \n \nYou are tailored for investors and traders looking to leverage technical analysis to enhance their trading strategies. By integrating these indicators, users can gain a comprehensive understanding of stock performance and market trends, enabling more informed decision-making."

RESPONSE_COLLECTION = "sessions"


class Message(CamelCaseModel):
    role: str
    message_text: str
    created_at: datetime


class ResponsesData(CamelCaseModel):
    messages: List[Message]


class UserMessageRequest(CamelCaseModel):
    session_id: str
    message: str


@router.post("")
async def main(request: UserMessageRequest):
    """
    Handles user messages, interacts with OpenAI, and manages session data.

    Args:
        msg (str): The user's input message.

    Returns:
        dict: The final response from OpenAI or the result of tool calls.

    Workflow:
    1. Creates a new session ID and saves the initial message to the database.
    2. Sends the message to OpenAI and processes the response.
    3. If the response is a final plain text answer, it updates the database and returns the response.
    4. If the response includes tool calls, it processes each tool call, updates the database, and continues the loop.
    5. Handles errors and logs them appropriately.
    """
    db = get_database()
    session_id = request.session_id

    input_messages = [
        {
            "role": "user",
            "content": [{"type": "input_text", "text": request.message}],
        },
    ]

    db[RESPONSE_COLLECTION].update_one(
        {"session_id": session_id, "messages": {"$exists": False}},
        {"$set": {"messages": []}},
    )

    db[RESPONSE_COLLECTION].update_one(
        {"session_id": session_id},
        {
            "$push": {
                "messages": {
                    "role": "user",
                    "messageText": request.message,
                    "created_at": datetime.now(timezone.utc),
                }
            }
        },
    )

    logger.info("Starting main function.")
    messagesCopy = input_messages.copy()

    try:
        while True:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=messagesCopy,
                tools=tools,
                store=True,
                instructions=instructions,
            )

            logger.info("Response received from OpenAI.")

            # If final answer is returned as plain text
            # if isinstance(response.output, str):
            #     logger.info("Final response received.")

            #     # Update the database with the final response
            #     db[RESPONSE_COLLECTION].update_one(
            #         {"session_id": session_id},
            #         {"$set": {"final_response": response.output}},
            #     )

            #     return {"response": response.output}

            # Handle all tool calls in the output
            tool_calls = [
                tool for tool in response.output if tool.type == "function_call"
            ]

            if not tool_calls:
                logger.warning("No function calls in response.")
                role = response.output[0].role
                message_text = response.output[0].content[0].text
                # Remove the conflicting `messages` field

                # Step 1: Make sure 'messages' exists
                db[RESPONSE_COLLECTION].update_one(
                    {"session_id": session_id, "messages": {"$exists": False}},
                    {"$set": {"messages": []}},
                )

                # Step 2: Push message
                db[RESPONSE_COLLECTION].update_one(
                    {"session_id": session_id},
                    {
                        "$push": {
                            "messages": {
                                "role": role,
                                "message_text": message_text,
                                "created_at": datetime.now(timezone.utc),
                            }
                        }
                    },
                )

                return {
                    "messages": [
                        {
                            "role": response.output[0].role,
                            "messageText": response.output[0].content[0].text,
                            "created_at": datetime.now(timezone.utc),
                        }
                    ]
                }

            for tool_call in tool_calls:
                name = tool_call.name
                args = json.loads(tool_call.arguments)

                logger.debug(f"Calling tool: {name} with args: {args}")
                result = await handle_tool_outputs(name, args)

                await asyncio.sleep(1)
                # Append tool call and its output to messages
                messagesCopy.append(tool_call)  # append model's function call message
                messagesCopy.append(  # append result message
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": str(result),
                    }
                )

            logger.info("Tool call(s) processed; continuing loop for next round.")

    except Exception as e:
        logger.error(f"Error creating message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{session_id}", response_model=ResponsesData)
async def get_responses(session_id: str, db: Database = Depends(get_database)):
    """
    Retrieves all messages for a given session ID.
    """
    try:
        session = db[RESPONSE_COLLECTION].find_one({"session_id": session_id}) or {}

        messages = session.get("messages", [])
        logger.info(f"Retrieved {len(messages)} message(s) for session_id={session_id}")

        return {"messages": messages}

    except PyMongoError as e:
        logger.error(
            f"Database error while retrieving session {session_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages",
        )
