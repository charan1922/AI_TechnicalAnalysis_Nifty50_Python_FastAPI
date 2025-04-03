get_stock_ma_tool = {
    "type": "function",
    "name": "getStockMA",
    "description": "Get the Moving Average (MA) of the stock based on the symbol and period. The period is optional and defaults to 50 days.",
    "strict": False,
    "parameters": {
        "type": "object",
        "properties": {
            "stockSymbol": {
                "type": "string",
                "description": "The stock symbol (e.g., WIPRO for WIPRO LTD.)",
            },
            "period": {
                "type": "integer",
                "description": "The period for the Moving Average. Defaults to 50.",
                "default": 50,
            },
        },
        "additionalProperties": False,
        "required": ["stockSymbol"],
    },
}
