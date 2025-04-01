from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
Fibonacci Retracement is a technical analysis tool used to identify potential levels of support and resistance in a price trend. Based on the Fibonacci sequence, the tool involves plotting horizontal lines at key Fibonacci levels, which are derived from the ratios of the sequence. These levels are used to forecast potential reversal points in the market.

The key Fibonacci retracement levels are 23.6%, 38.2%, 50%, 61.8%, and 76.4%. These levels are calculated by taking the difference between a high and a low price and then applying the Fibonacci ratios to this range. For example, if a stock rises from a low of $100 to a high of $150, the Fibonacci retracement levels would be calculated as follows:
- 23.6% level: $150 - (0.236 * ($150 - $100))
- 38.2% level: $150 - (0.382 * ($150 - $100))
- 50% level: $150 - (0.50 * ($150 - $100))
- 61.8% level: $150 - (0.618 * ($150 - $100))

Traders use these levels to anticipate where a price might pull back to before continuing in the direction of the trend. Fibonacci retracement levels are commonly used to gauge potential entry and exit points, assess market sentiment, and identify potential reversal areas.
"""

def calculate_fibonacci_retracement(data):
    """
    Calculate Fibonacci Retracement levels for given stock data
    """
    if len(data) < 2:
        return "Not enough data to calculate Fibonacci Retracement"

    # Extract high and low prices
    highest_high = max(item["High"] for item in data)
    lowest_low = min(item["Low"] for item in data)

    # Calculate retracement levels
    price_range = highest_high - lowest_low
    retracement_levels = {
        "0%": highest_high,
        "23.6%": highest_high - (price_range * 0.236),
        "38.2%": highest_high - (price_range * 0.382),
        "50%": highest_high - (price_range * 0.5),
        "61.8%": highest_high - (price_range * 0.618),
        "100%": lowest_low,
    }

    return retracement_levels

async def calculate_stock_fibonacci_retracement(function_arguments):
    """
    Calculate Fibonacci Retracement levels for a given stock symbol
    """
    try:
        logger.info("Calculating Fibonacci Retracement... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]

        logger.info(
            "Calculating Fibonacci Retracement for stock: %s",
            stock_symbol
        )

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate Fibonacci Retracement levels
        retracement_levels = calculate_fibonacci_retracement(stock_data)

        logger.info("Fibonacci Retracement calculated successfully for stock: %s", stock_symbol)
        return {
            "retracementLevels": retracement_levels,
            "description": DESCRIPTION
        }

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating Fibonacci Retracement: %s", str(e))
        raise Exception(f"Error calculating Fibonacci Retracement: {str(e)}")