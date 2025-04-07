get_stock_vwap_tool = {
    "type": "function",
    "name": "getStockVWAP",
    "description": "Get the Volume Weighted Average Price (VWAP) of the stock based on the symbol.",
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
