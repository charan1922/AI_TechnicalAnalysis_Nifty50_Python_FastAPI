from openai import OpenAI
import json
import os
from app.tools.tools import tools
from app.utils.function_handlers import handle_tool_outputs
import asyncio
from app.core.openai import client
from app.core.logger import logging

logger = logging.getLogger(__name__)

input_messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "input_text",
                "text": "You are designed to provide comprehensive technical analysis for the top 50 stocks in the Nifty index. You offer insights on various technical indicators to aid in making informed buying and selling decisions. \n \nYou are tailored for investors and traders looking to leverage technical analysis to enhance their trading strategies. By integrating these indicators, users can gain a comprehensive understanding of stock performance and market trends, enabling more informed decision-making.",
            }
        ],
    },
    {
        "role": "user",
        "content": [{"type": "input_text", "text": "price of TCS"}],
    },
]


async def main():
    logger.info("Starting main function.")
    response = client.responses.create(
        model="gpt-4o-mini",
        input=input_messages,
        tools=tools,
        store=True,
    )
    logger.info("Initial response received from OpenAI.")

    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue

        name = tool_call.name
        args = json.loads(tool_call.arguments)
        logger.debug(f"Processing tool call: {name} with arguments: {args}")

        result = await handle_tool_outputs(name, args)
        logger.info(f"Tool call {name} executed successfully with result: {result}")

        input_messages.append(tool_call)
        input_messages.append(
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": str(result),
            }
        )

    logger.info("Preparing second response with updated input messages.")
    response_2 = client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools,
    )
    logger.info("Final response received from OpenAI.")
    print(response_2.output_text)


if __name__ == "__main__":
    asyncio.run(main())
