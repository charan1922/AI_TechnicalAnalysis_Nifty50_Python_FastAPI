get_stock_obv_tool = {
    "type": "function",
    "name": "getStockOBV",
    "description": "Get the On-Balance Volume (OBV) of the stock based on the symbol.",
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
