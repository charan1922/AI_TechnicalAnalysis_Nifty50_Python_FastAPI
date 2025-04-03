# Import individual tool definitions
from .get_stock_price import get_stock_price_tool
from .get_stock_symbol import get_stock_symbol_tool
from .get_stock_ma import get_stock_ma_tool
from .get_stock_rsi import get_stock_rsi_tool
from .get_stock_macd import get_stock_macd_tool


# List of available tools
# Add new tools here as needed
tools = [
    get_stock_price_tool,  # Tool for fetching stock price
    get_stock_symbol_tool,  # Tool for fetching stock symbol
    get_stock_ma_tool,  # Tool for fetching moving average
    get_stock_rsi_tool,  # Tool for fetching RSI
    get_stock_macd_tool,  # Tool for fetching MACD
]
