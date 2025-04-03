get_stock_fibonacci_retracement_tool = {
    "type": "function",
    "name": "getStockFibonacciRetracement",
    "description": "Get the Fibonacci Retracement levels of the stock based on the symbol.",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "stockSymbol": {
                "type": "string",
                "description": "The stock symbol (e.g., WIPRO for WIPRO LTD.)",
            }
        },
        "additionalProperties": False,  # Disallow extra parameters
        "required": ["stockSymbol"],
    },
}
