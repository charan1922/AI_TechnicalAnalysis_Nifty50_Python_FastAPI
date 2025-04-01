from app.utils.stock_information import stock_collection
from app.core.logger import logging


logger = logging.getLogger(__name__)
# Description constant
DESCRIPTION = """
A Moving Average (MA) is a technical analysis indicator that helps identify the direction of a trend by smoothing out price data. It is calculated by averaging the closing prices of a stock over a specified period. There are different types of moving averages, including the Simple Moving Average (SMA) and the Exponential Moving Average (EMA).

The Simple Moving Average (SMA) calculates the average of closing prices over a defined number of periods, such as 20, 50, or 200 days. The Exponential Moving Average (EMA) gives more weight to recent prices and reacts more quickly to price changes than the SMA.

Moving Averages are used to identify the direction of the trend, potential support and resistance levels, and to smooth out price fluctuations. Crossovers between short-term and long-term moving averages can signal potential buy or sell opportunities. For example, when a short-term MA crosses above a long-term MA, it may indicate a bullish trend, while a crossover below may suggest a bearish trend.
"""


def calculate_moving_average(data, period):
    """
    Calculate simple moving average for given data and period
    """
    if len(data) < period:
        return "Not enough data"

    sum_prices = sum(item["Close"] for item in data[:period])
    return sum_prices / period


async def calculate_stock_ma(function_arguments):
    """
    Calculate moving average for a given stock symbol
    """
    try:
        logger.info("Calculating moving average... %s", function_arguments)
        # Access as dictionary keys
        stock_symbol = function_arguments["stockSymbol"]
        period = function_arguments.get("period", 50)

        logger.info(
            "Calculating moving average for stock: %s with period: %s",
            stock_symbol,
            period,
        )

        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)
        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate moving average
        moving_average = calculate_moving_average(stock_data, period)

        logger.info(
            "Moving average calculated successfully for stock: %s", stock_symbol
        )
        return {
            "moving_average": moving_average,
            "period": period,
            "description": DESCRIPTION,
        }
    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating stock MA: %s", str(e))
        raise Exception(f"Error calculating stock MA: {str(e)}")
