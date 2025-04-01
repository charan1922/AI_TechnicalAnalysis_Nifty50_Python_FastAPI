from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements. RSI values range from 0 to 100 and are used to identify overbought or oversold conditions in a market. Typically, an RSI value above 70 suggests that a stock may be overbought and could be due for a price correction or pullback, while an RSI value below 30 indicates that a stock may be oversold and could be poised for a rebound or upward movement.

RSI is calculated using the average gains and losses over a specified period, commonly 14 days. The RSI line oscillates between these extreme values, providing insights into potential reversal points or the strength of the current trend. Traders use RSI to spot potential buy or sell signals and to gauge the momentum behind price movements.
"""


def calculate_average_gain_loss(stock_data, period):
    """
    Calculate average gain and loss over the specified period
    """
    gains = 0
    losses = 0

    for i in range(1, period + 1):
        change = stock_data[i]["Close"] - stock_data[i - 1]["Close"]
        if change > 0:
            gains += change
        else:
            losses -= change  # Losses are kept as positive numbers

    average_gain = gains / period
    average_loss = losses / period

    return {"averageGain": average_gain, "averageLoss": average_loss}


async def calculate_stock_rsi(function_arguments):
    """
    Calculate RSI for a given stock symbol
    """
    try:
        logger.info("Calculating RSI... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]
        period = function_arguments.get("period", 14)

        logger.info(
            "Calculating RSI for stock: %s with period: %s", stock_symbol, period
        )

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        if len(stock_data) < period:
            raise Exception("Not enough data points to calculate RSI")

        # Calculate initial RSI
        averages = calculate_average_gain_loss(stock_data, period)
        rs = (
            averages["averageGain"] / averages["averageLoss"]
            if averages["averageLoss"] != 0
            else float("inf")
        )
        rsi = 100 - (100 / (1 + rs)) if rs != float("inf") else 100

        # Uncomment and adapt this section if you want to calculate RSI for all periods
        """
        rsi_array = []
        avg_gain = averages["averageGain"]
        avg_loss = averages["averageLoss"]

        for i in range(period + 1, len(stock_data)):
            change = stock_data[i]["Close"] - stock_data[i - 1]["Close"]
            if change > 0:
                avg_gain = (avg_gain * (period - 1) + change) / period
                avg_loss = (avg_loss * (period - 1)) / period
            else:
                avg_gain = (avg_gain * (period - 1)) / period
                avg_loss = (avg_loss * (period - 1) - change) / period
            
            rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
            current_rsi = 100 - (100 / (1 + rs)) if rs != float('inf') else 100
            rsi_array.append({"Date": stock_data[i]["Date"], "RSI": current_rsi})
        """

        logger.info("RSI calculated successfully for stock: %s", stock_symbol)
        return {"rsi": rsi, "description": DESCRIPTION, "period": period}

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating RSI: %s", str(e))
        raise Exception(f"Error calculating RSI: {str(e)}")
