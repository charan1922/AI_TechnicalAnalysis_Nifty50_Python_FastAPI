get_stock_rsi_tool = {
    "type": "function",
    "name": "getStockRSI",
    "description": "Get the RSI of the stock based on the symbol and period. The period is optional and defaults to 14.",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "stockSymbol": {
                "type": "string",
                "description": "The stock symbol (e.g., WIPRO for WIPRO LTD.)",
            },
            "period": {
                "type": "number",
                "description": "Number of days for calculating the RSI",
                "default": 14,
            },
        },
        "additionalProperties": False,  # Disallow extra parameters
        "required": ["stockSymbol"],
    },
}
