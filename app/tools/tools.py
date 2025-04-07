# Import individual tool definitions
from .get_stock_adx import get_stock_adx_tool
from .get_stock_bollinger_bands import get_stock_bollinger_bands_tool
from .get_stock_fibonacci_retracement import get_stock_fibonacci_retracement_tool
from .get_stock_ichimoku_cloud import get_stock_ichimoku_cloud_tool
from .get_stock_ma import get_stock_ma_tool
from .get_stock_macd import get_stock_macd_tool
from .get_stock_obv import get_stock_obv_tool
from .get_stock_price import get_stock_price_tool
from .get_stock_rsi import get_stock_rsi_tool
from .get_stock_stochastic_oscillator import get_stock_stochastic_oscillator_tool
from .get_stock_vwap import get_stock_vwap_tool
from .get_stock_symbol import get_stock_symbol_tool

# List of available tools
# Add new tools here as needed
tools = [
    get_stock_price_tool,  # Tool for fetching stock price
    get_stock_symbol_tool,  # Tool for fetching stock symbol
    get_stock_ma_tool,  # Tool for fetching moving average
    get_stock_rsi_tool,  # Tool for fetching RSI
    get_stock_macd_tool,  # Tool for fetching MACD
    get_stock_obv_tool,  # Tool for fetching OBV
    get_stock_ichimoku_cloud_tool,  # Tool for fetching Ichimoku Cloud
    get_stock_bollinger_bands_tool,  # Tool for fetching Bollinger Bands
    get_stock_adx_tool,  # Tool for fetching ADX
    get_stock_fibonacci_retracement_tool,  # Tool for fetching Fibonacci Retracement
    get_stock_stochastic_oscillator_tool,  # Tool for fetching Stochastic Oscillator
]
