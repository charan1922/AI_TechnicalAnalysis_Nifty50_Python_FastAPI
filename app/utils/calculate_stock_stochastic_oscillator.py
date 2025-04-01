from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
The Stochastic Oscillator is a momentum indicator that compares a particular closing price of a security to its price range over a specified period. It consists of two lines: %K and %D. The %K line represents the current closing price relative to the high-low range over a set period, while the %D line is a moving average of the %K line.

Typically, the %K line is calculated over a 14-day period and is plotted alongside the %D line, which is usually a 3-day moving average of %K. Values for the Stochastic Oscillator range from 0 to 100. Readings above 80 are considered overbought, indicating that the price may be due for a pullback, while readings below 20 are considered oversold, suggesting that the price may be poised for a rebound.

Traders use the Stochastic Oscillator to identify potential reversal points, assess market momentum, and confirm other technical indicators. The crossing of the %K and %D lines can signal potential buy or sell opportunities.
"""


def calculate_stochastic_oscillator(data):
    """
    Calculate %K of Stochastic Oscillator based on full dataset
    """
    if len(data) < 14:
        return "Not enough data to calculate Stochastic Oscillator"

    highest_high = max(item["High"] for item in data)
    lowest_low = min(item["Low"] for item in data)
    current_close = data[0]["Close"]

    percent_k = (
        ((current_close - lowest_low) / (highest_high - lowest_low)) * 100
        if highest_high != lowest_low
        else 0
    )

    return percent_k


async def calculate_stock_stochastic_oscillator(function_arguments):
    """
    Calculate Stochastic Oscillator %K for a given stock symbol
    """
    try:
        logger.info("Calculating Stochastic Oscillator... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]

        logger.info("Calculating Stochastic Oscillator for stock: %s", stock_symbol)

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate Stochastic Oscillator %K
        percent_k = calculate_stochastic_oscillator(stock_data)

        logger.info(
            "Stochastic Oscillator calculated successfully for stock: %s", stock_symbol
        )
        return {"percentK": percent_k, "description": DESCRIPTION}

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating Stochastic Oscillator: %s", str(e))
        raise Exception(f"Error calculating Stochastic Oscillator: {str(e)}")
