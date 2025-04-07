get_stock_adx_tool = {
    "type": "function",
    "name": "getStockADX",
    "description": "The Average Directional Index (ADX) is a technical analysis indicator used to quantify the strength of a trend.",
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
                "description": "The period for the ADX. Defaults to 14.",
                "default": 14,
            },
        },
        "additionalProperties": False,  # Disallow extra parameters
        "required": ["stockSymbol"],
    },
}
