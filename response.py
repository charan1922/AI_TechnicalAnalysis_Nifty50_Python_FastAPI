from openai import OpenAI
import json
import os
from app.tools.tools import tools
from app.utils.function_handlers import handle_tool_outputs
import asyncio
from app.core.logger import logging

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

logger = logging.getLogger(__name__)

instructions = "You are designed to provide comprehensive technical analysis for the top 50 stocks in the Nifty index. You offer insights on various technical indicators to aid in making informed buying and selling decisions. \n \nYou are tailored for investors and traders looking to leverage technical analysis to enhance their trading strategies. By integrating these indicators, users can gain a comprehensive understanding of stock performance and market trends, enabling more informed decision-making."

input_messages = [
    {
        "role": "user",
        "content": [
            {"type": "input_text", "text": "do the technical analysis of hdfc"}
        ],
    },
]


async def main():
    logger.info("Starting main function.")
    messages = input_messages.copy()

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
            print(response.output, ":final response")
            break

        # Handle all tool calls in the output
        # tool_calls = [tool for tool in response.output if tool.type == "function_call"]

        tool_calls = []
        for tool in response.output:
            if tool.type == "function_call":
                tool_calls.append(tool)
        # print(tool_calls, ":tool calls")
        if not tool_calls:
            print(response.output, ":no function calls")
            break

        for tool_call in tool_calls:
            name = tool_call.name
            args = json.loads(tool_call.arguments)

            logger.debug(f"Calling tool: {name} with args: {args}")
            result = await handle_tool_outputs(name, args)

            await asyncio.sleep(2)
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


if __name__ == "__main__":
    asyncio.run(main())
