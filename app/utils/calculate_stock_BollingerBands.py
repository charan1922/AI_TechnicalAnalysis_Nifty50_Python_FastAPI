from app.utils.stock_information import stock_collection
from app.core.logger import logging
import math

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
Bollinger Bands are a volatility indicator that consists of three lines plotted on a price chart: a middle line, which is a simple moving average (SMA) of the stock price, and two outer bands that are standard deviations away from the SMA. The outer bands adjust to market volatility, expanding when volatility increases and contracting when volatility decreases.

Typically, the middle band is set to a 20-day SMA, while the outer bands are calculated by adding and subtracting two standard deviations from the SMA. When the price approaches or crosses the upper band, it may indicate that the stock is overbought, while touching or crossing the lower band may suggest that the stock is oversold.

Bollinger Bands are used to identify potential price breakouts, trend reversals, and periods of high or low volatility. Traders often use Bollinger Bands in conjunction with other indicators to make more informed trading decisions.
"""

def calculate_bollinger_bands(data, period=20, multiplier=2):
    """
    Calculate Bollinger Bands for given stock data
    """
    if len(data) < period:
        return "Not enough data to calculate Bollinger Bands"

    moving_averages = []
    standard_deviations = []
    upper_bands = []
    lower_bands = []

    # Calculate SMA, std dev, and bands for each window
    for i in range(len(data) - period + 1):
        # Calculate Simple Moving Average
        window = data[i:i + period]
        sma = sum(item["Close"] for item in window) / period
        moving_averages.append(sma)

        # Calculate variance and standard deviation
        squared_differences = [(item["Close"] - sma) ** 2 for item in window]
        variance = sum(squared_differences) / period
        std_dev = math.sqrt(variance)
        standard_deviations.append(std_dev)

        # Calculate upper and lower bands
        upper_bands.append(sma + multiplier * std_dev)
        lower_bands.append(sma - multiplier * std_dev)

    # Return the latest values
    latest_index = len(moving_averages) - 1
    return {
        "movingAverage": moving_averages[latest_index],
        "upperBand": upper_bands[latest_index],
        "lowerBand": lower_bands[latest_index]
    }

async def calculate_stock_bollinger_bands(function_arguments):
    """
    Calculate Bollinger Bands for a given stock symbol
    """
    try:
        logger.info("Calculating Bollinger Bands... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]
        period = function_arguments.get("period", 20)
        multiplier = function_arguments.get("multiplier", 2)

        logger.info(
            "Calculating Bollinger Bands for stock: %s with period: %s and multiplier: %s",
            stock_symbol,
            period,
            multiplier
        )

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate Bollinger Bands
        bollinger_bands_data = calculate_bollinger_bands(stock_data, period, multiplier)

        logger.info("Bollinger Bands calculated successfully for stock: %s", stock_symbol)
        return {
            "bollingerBandsData": bollinger_bands_data,
            "period": period,
            "multiplier": multiplier,
            "description": DESCRIPTION
        }

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating Bollinger Bands: %s", str(e))
        raise Exception(f"Error calculating Bollinger Bands: {str(e)}")