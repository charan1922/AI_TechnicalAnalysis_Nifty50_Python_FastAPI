# Tool definition for fetching stock prices
get_stock_price_tool = {
    "type": "function",
    "name": "getStockPrice",
    "description": "Retrieve the current stock price using the stock symbol.",
    "strict": True,  # Enforce strict parameter validation
    "parameters": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "The stock symbol (e.g., 'AAPL' for Apple Inc.).",
            }
        },
        "additionalProperties": False,  # Disallow extra parameters
        "required": ["symbol"],  # Ensure 'symbol' is always provided
    },
}
