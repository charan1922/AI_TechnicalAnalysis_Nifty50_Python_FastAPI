from openai import OpenAI
import json
import os
from app.tools.tools import tools
from app.utils.function_handlers import handle_tool_outputs
import asyncio  # Add asyncio for handling asynchronous calls

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


def get_stock_price(symbol):
    return {"price": 100, "symbol": symbol}


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
    response = client.responses.create(
        model="gpt-4o-mini",
        input=input_messages,
        tools=tools,
        # text={"format": {"type": "text"}},
        store=True,
    )

    # print(response.output, ":-----------------response")

    # tool_call = response.output[0]
    # args = json.loads(tool_call.arguments)

    # # print(args, ":-----------------args")
    # result = get_stock_price(args["symbol"])

    # # print(response.output, ":-----------------response output")

    for tool_call in response.output:
        if tool_call.type != "function_call":
            continue

        name = tool_call.name
        args = json.loads(tool_call.arguments)  # parse the arguments from JSON
        # print(args, ":-----------------args")

        result = await handle_tool_outputs(name, args)  # Await the coroutine
        input_messages.append(tool_call)  # append the tool call message
        input_messages.append(
            {  # append result message
                "type": "function_call_output",
                "call_id": tool_call.call_id,  # ensure call_id matches the tool call
                "output": str(result),
            }
        )

    # print(input_messages, ":-----------------input messages")
    response_2 = client.responses.create(
        model="gpt-4o",
        input=input_messages,
        tools=tools,
    )
    print(response_2.output_text)  # Print the final output


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
