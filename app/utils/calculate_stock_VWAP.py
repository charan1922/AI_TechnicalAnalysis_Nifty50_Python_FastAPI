from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
The Volume Weighted Average Price (VWAP) is a trading benchmark that provides the average price a stock has traded at throughout the day, based on both volume and price. VWAP is calculated by taking the sum of the product of the price and volume for each transaction and then dividing by the total volume for the period.

VWAP is used to assess the current trading price relative to the average price for the day, helping traders determine the trend direction and the value of the stock at various points throughout the trading day. It is often used as a reference point to gauge the market trend, make buy or sell decisions, and assess the execution quality of trades. VWAP can act as a support or resistance level, and traders may use it to confirm trends and manage risk.
"""


def calculate_vwap(data):
    """
    Calculate VWAP using the latest data point only
    """
    if len(data) == 0:
        return "Not enough data to calculate VWAP"

    # Use only the latest data point
    latest_data = data[0]
    typical_price = (
        latest_data["High"] + latest_data["Low"] + latest_data["Close"]
    ) / 3
    volume = latest_data["Volume"]

    cumulative_tpv = typical_price * volume
    cumulative_volume = volume

    vwap = cumulative_tpv / cumulative_volume if cumulative_volume != 0 else 0
    return vwap


async def calculate_stock_vwap(function_arguments):
    """
    Calculate VWAP for a given stock symbol
    """
    try:
        logger.info("Calculating VWAP... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]

        logger.info("Calculating VWAP for stock: %s", stock_symbol)

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate VWAP
        vwap_value = calculate_vwap(stock_data)

        logger.info("VWAP calculated successfully for stock: %s", stock_symbol)
        return {"vwapValue": vwap_value, "description": DESCRIPTION}

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating VWAP: %s", str(e))
        raise Exception(f"Error calculating VWAP: {str(e)}")
