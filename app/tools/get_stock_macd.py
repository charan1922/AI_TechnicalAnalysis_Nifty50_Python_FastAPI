get_stock_macd_tool = {
    "type": "function",
    "name": "getStockMACD",
    "description": "Get the MACD of the stock based on the symbol and the short, long, and signal periods.",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "stockSymbol": {
                "type": "string",
                "description": "The stock symbol (e.g., WIPRO for WIPRO LTD.)",
            },
            "shortPeriod": {
                "type": "integer",
                "description": "The short period for the MACD. Defaults to 12.",
                "default": 12,
            },
            "longPeriod": {
                "type": "integer",
                "description": "The long period for the MACD. Defaults to 26.",
                "default": 26,
            },
            "signalPeriod": {
                "type": "integer",
                "description": "The signal period for the MACD. Defaults to 9.",
                "default": 9,
            },
        },
        "additionalProperties": False,
        "required": ["stockSymbol"],
    },
}
