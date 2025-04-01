from .calculate_stock_MA import calculate_stock_ma
from .calculate_stock_RSI import calculate_rsi as calculate_stock_rsi
from .calculate_stock_MACD import calculate_macd as calculate_stock_macd
from .calculate_stock_BollingerBands import (
    calculate_bollinger_bands as calculate_stock_bollinger_bands,
)
from .calculate_stock_StochasticOscillator import (
    calculate_stochastic_oscillator as calculate_stock_stochastic_oscillator,
)
from .calculate_stock_ADX import calculate_adx as calculate_stock_adx
from .calculate_stock_VWAP import calculate_vwap as calculate_stock_vwap

from .stock_information import (
    get_nifty_stock_symbol_info,
    get_stock_price,
    get_stocks_by_industry,
)


async def handle_tool_outputs(func_name, function_arguments):
    try:
        output = None
        if func_name == "getStockSymbol":
            output = await get_nifty_stock_symbol_info(
                function_arguments["stockName"]
            )  # Added await
        elif func_name == "getStockPrice":
            output = await get_stock_price(function_arguments["symbol"])  # Added await
        elif func_name == "getStocksByIndustry":
            output = await get_stocks_by_industry(
                function_arguments["symbol"]
            )  # Added await
        elif func_name == "getStockMA":
            output = await calculate_stock_ma(function_arguments)  # No await needed
        elif func_name == "getStockRSI":
            output = calculate_stock_rsi(function_arguments)  # No await needed
        elif func_name == "getStockMACD":
            output = calculate_stock_macd(function_arguments)  # No await needed
        elif func_name == "getStockBollingerBands":
            output = calculate_stock_bollinger_bands(
                function_arguments
            )  # No await needed
        elif func_name == "getStockStochasticOscillator":
            output = calculate_stock_stochastic_oscillator(
                function_arguments
            )  # No await needed
        elif func_name == "getStockADX":
            output = calculate_stock_adx(function_arguments)  # No await needed
        elif func_name == "getStockVWAP":
            output = calculate_stock_vwap(function_arguments)  # No await needed
        else:
            print("Function not found")
            output = f"Error: Function {func_name} not found"

        print(output, f":Output of {func_name}")
        return {"output": output}
    except Exception as error:
        print(str(error), f":Error in {func_name}")
        raise error
