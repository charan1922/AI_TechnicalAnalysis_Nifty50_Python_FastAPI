get_stock_bollinger_bands_tool = {
    "type": "function",
    "name": "getStockBollingerBands",
    "description": "Get the Bollinger Bands of the stock based on the symbol and period.",
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
                "description": "The period for the Bollinger Bands. Defaults to 20.",
                "default": 20,
            },
            "multiplier": {
                "type": "integer",
                "description": "The multiplier for the Bollinger Bands. Defaults to 2.",
                "default": 2,
            },
        },
        "additionalProperties": False,  # Disallow extra parameters
        "required": ["stockSymbol"],
    },
}
