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

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/response_api", tags=["response"])

instructions = "You are designed to provide comprehensive technical analysis for the top 50 stocks in the Nifty index. You offer insights on various technical indicators to aid in making informed buying and selling decisions. \n \nYou are tailored for investors and traders looking to leverage technical analysis to enhance their trading strategies. By integrating these indicators, users can gain a comprehensive understanding of stock performance and market trends, enabling more informed decision-making."

# input_messages = [{"role": "user", "content": "do the technical analysis of hdfc"}]


@router.post("/")
async def main(msg: str):
    input_messages = [
        {
            "role": "user",
            "content": [{"type": "input_text", "text": msg}],
        },
    ]
    logger.info("Starting main function.")
    messages = input_messages.copy()

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

            logger.info("Tool call(s) processed; continuing loop for next round.")

    except Exception as e:
        logger.error(f"Error creating message: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
