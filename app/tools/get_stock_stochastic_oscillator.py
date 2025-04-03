get_stock_stochastic_oscillator_tool = {
    "type": "function",
    "name": "getStockStochasticOscillator",
    "description": "Get the Stochastic Oscillator of the stock based on the symbol and period.",
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
                "description": "The period for the Stochastic Oscillator. Defaults to 14.",
                "default": 14,
            },
        },
        "additionalProperties": False,  # Disallow extra parameters
        "required": ["stockSymbol"],
    },
}
