# Tool definition for fetching stock symbols
get_stock_symbol_tool = {
    "type": "function",
    "name": "getStockSymbol",
    "description": "Retrieve the stock symbol based on the provided stock name.",
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            "stockName": {
                "type": "string",
                "description": "The name of the stock (e.g., 'WIPRO' for WIPRO LTD).",
            }
        },
        "additionalProperties": False,  # Disallow extra parameters
        "required": ["stockName"],  # Ensure 'stockName' is always provided
    },
}
