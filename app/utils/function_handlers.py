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

from .stock_information import (
    get_nifty_stock_symbol_info,
    get_stock_price,
    get_stocks_by_industry,
)


async def handle_tool_outputs(func_name, function_arguments):
    try:
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
            print("Function not found")
            output = f"Error: Function {func_name} not found"

        print(output, f":Output of {func_name}")
        return {"output": output}
    except Exception as error:
        print(str(error), f":Error in {func_name}")
        raise error
