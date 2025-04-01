from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
The Moving Average Convergence Divergence (MACD) is a trend-following momentum indicator that shows the relationship between two moving averages of a stock's price. It is calculated by subtracting the 26-period Exponential Moving Average (EMA) from the 12-period EMA, resulting in the MACD line. A 9-period EMA of the MACD line, known as the signal line, is then plotted on top of the MACD line to act as a trigger for buy and sell signals.

The MACD is used to identify potential buy and sell opportunities based on the convergence and divergence of the MACD line and the signal line. When the MACD line crosses above the signal line, it may indicate a bullish signal, suggesting that it might be a good time to buy. Conversely, when the MACD line crosses below the signal line, it may indicate a bearish signal, suggesting that it might be a good time to sell.

Additionally, the distance between the MACD line and the signal line can provide insights into the strength of the trend, while the histogram (the difference between the MACD line and the signal line) can indicate the momentum behind the trend.
"""


def calculate_ema(data, period):
    """
    Calculate Exponential Moving Average for given data and period
    """
    k = 2 / (period + 1)
    ema_array = [data[0]["Close"]]  # Start with the first closing price

    for i in range(1, len(data)):
        ema = data[i]["Close"] * k + ema_array[i - 1] * (1 - k)
        ema_array.append(ema)

    return ema_array


def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    """
    Calculate MACD components for given stock data
    """
    if len(data) < long_period:
        return "Not enough data to calculate MACD"

    # Calculate short and long EMAs
    short_ema = calculate_ema(data, short_period)
    long_ema = calculate_ema(data, long_period)

    # Calculate MACD line
    macd_line = [short - long for short, long in zip(short_ema, long_ema)]

    # Calculate signal line using the MACD line
    signal_start_index = long_period - short_period
    signal_line = calculate_ema(
        [{"Close": x} for x in macd_line[signal_start_index:]], signal_period
    )

    # Calculate MACD histogram
    macd_histogram = [
        macd - signal
        for macd, signal in zip(macd_line[signal_start_index:], signal_line)
    ]

    return {
        "macdLine": macd_line[signal_start_index:],
        "signalLine": signal_line,
        "macdHistogram": macd_histogram,
    }


async def calculate_stock_macd(function_arguments):
    """
    Calculate MACD for a given stock symbol
    """
    try:
        logger.info("Calculating MACD... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]
        short_period = function_arguments.get("shortPeriod", 12)
        long_period = function_arguments.get("longPeriod", 26)
        signal_period = function_arguments.get("signalPeriod", 9)

        logger.info(
            "Calculating MACD for stock: %s with periods: %s, %s, %s",
            stock_symbol,
            short_period,
            long_period,
            signal_period,
        )

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate MACD
        macd = calculate_macd(stock_data, short_period, long_period, signal_period)

        logger.info("MACD calculated successfully for stock: %s", stock_symbol)
        return {"macd": macd, "description": DESCRIPTION}

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating stock MACD: %s", str(e))
        raise Exception(f"Error calculating stock MACD: {str(e)}")
