from .calculate_stock_MA import calculate_stock_ma
from .calculate_stock_RSI import calculate_stock_rsi
from .calculate_stock_MACD import calculate_stock_macd
from .calculate_stock_BollingerBands import calculate_stock_bollinger_bands
from .calculate_stock_fibonacci_retracement import calculate_stock_fibonacci_retracement
from .calculate_stock_ichimoku_cloud import calculate_stock_ichimoku_cloud
from .calculate_stock_obv import calculate_stock_obv
from .calculate_stock_stochastic_oscillator import calculate_stock_stochastic_oscillator
from .calculate_stock_ADX import calculate_stock_adx
from .calculate_stock_VWAP import calculate_stock_vwap
from app.core.logger import logging
from bson import ObjectId  # Import for ObjectId handling

from .stock_information import (
    get_nifty_stock_symbol_info,
    get_stock_price,
    get_stocks_by_industry,
)

logger = logging.getLogger(__name__)


def convert_objectid_to_str(data):
    """
    Recursively convert ObjectId to string in a dictionary or list.
    """
    if isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data


async def handle_tool_outputs(func_name, function_arguments):
    try:
        logger.info("Handling tool output for function: %s", func_name)
        output = None
        if func_name == "getStockSymbol":
            output = await get_nifty_stock_symbol_info(function_arguments["stockName"])
        elif func_name == "getStockPrice":
            output = await get_stock_price(function_arguments["symbol"])  # Added await
        elif func_name == "getStocksByIndustry":
            output = await get_stocks_by_industry(function_arguments["symbol"])
        elif func_name == "getStockMA":
            output = await calculate_stock_ma(function_arguments)
        elif func_name == "getStockRSI":
            output = await calculate_stock_rsi(function_arguments)
        elif func_name == "getStockMACD":
            output = await calculate_stock_macd(function_arguments)
        elif func_name == "getStockBollingerBands":
            output = await calculate_stock_bollinger_bands(function_arguments)
        elif func_name == "getStockFibonacciRetracement":
            output = await calculate_stock_fibonacci_retracement(function_arguments)
        elif func_name == "getStockIchimokuCloud":
            output = await calculate_stock_ichimoku_cloud(function_arguments)
        elif func_name == "getStockStochasticOscillator":
            output = await calculate_stock_stochastic_oscillator(function_arguments)
        elif func_name == "getStockOBV":
            output = await calculate_stock_obv(function_arguments)
        elif func_name == "getStockADX":
            output = await calculate_stock_adx(function_arguments)
        elif func_name == "getStockVWAP":
            output = await calculate_stock_vwap(function_arguments)  # No await needed
        else:
            logger.error("Function not found: %s", func_name)
            output = f"Error: Function {func_name} not found"

        # Convert ObjectId to string before logging or returning
        output = convert_objectid_to_str(output)
        logger.info("Output of %s: %s", func_name, output)
        return {"output": output}
    except Exception as error:
        logger.error("Error in %s: %s", func_name, str(error))
        raise error
