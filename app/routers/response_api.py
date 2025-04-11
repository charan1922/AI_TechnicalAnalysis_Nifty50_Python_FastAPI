from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from app.utils.function_handlers import handle_tool_outputs
from app.core.openai import client
from app.core.config import settings
from app.core.logger import logging
from typing import Dict, Any
from pydantic import BaseModel
import asyncio
from app.tools.tools import tools
import json
from app.core.database import get_database
from bson import ObjectId

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/response_api", tags=["response"])

instructions = "You are designed to provide comprehensive technical analysis for the top 50 stocks in the Nifty index. You offer insights on various technical indicators to aid in making informed buying and selling decisions. \n \nYou are tailored for investors and traders looking to leverage technical analysis to enhance their trading strategies. By integrating these indicators, users can gain a comprehensive understanding of stock performance and market trends, enabling more informed decision-making."


@router.post("/")
async def main(msg: str):
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
    session_id = str(ObjectId())
    input_messages = [
        {
            "role": "user",
            "content": [{"type": "input_text", "text": msg}],
        },
    ]
    logger.info("Starting main function.")
    messages = input_messages.copy()

    # Save initial session and messages to the database
    db.sessions.insert_one({"session_id": session_id, "messages": messages})

    try:
        while True:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=messages,
                tools=tools,
                store=True,
                instructions=instructions,
            )

            logger.info("Response received from OpenAI.")

            # If final answer is returned as plain text
            if isinstance(response.output, str):
                logger.info("Final response received.")

                # Update the database with the final response
                db.sessions.update_one(
                    {"session_id": session_id},
                    {"$set": {"final_response": response.output}},
                )

                return {"response": response.output}

            # Handle all tool calls in the output
            tool_calls = [
                tool for tool in response.output if tool.type == "function_call"
            ]

            if not tool_calls:
                logger.warning("No function calls in response.")
                return {"result": response.output}

            for tool_call in tool_calls:
                name = tool_call.name
                args = json.loads(tool_call.arguments)

                logger.debug(f"Calling tool: {name} with args: {args}")
                result = await handle_tool_outputs(name, args)

                await asyncio.sleep(1)
                # Append tool call and its output to messages
                messages.append(tool_call)
                messages.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": str(result),
                    }
                )

                # Save only the function_call_output data to the database
                db.sessions.update_one(
                    {"session_id": session_id},
                    {
                        "$push": {
                            "messages": {
                                "type": "function_call_output",
                                "call_id": tool_call.call_id,
                                "output": str(result),
                            }
                        }
                    },
                )

            logger.info("Tool call(s) processed; continuing loop for next round.")

    except Exception as e:
        logger.error(f"Error creating message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
