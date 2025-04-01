from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
On-Balance Volume (OBV) is a volume-based indicator that uses volume flow to predict changes in stock price. The OBV line is calculated by adding the volume of a stock to the previous OBV value when the price closes higher and subtracting the volume when the price closes lower. This cumulative total helps to gauge the strength of a price trend.

The core principle of OBV is that volume precedes price movement; thus, increasing OBV values suggest that buying pressure is strong and may lead to higher prices, while decreasing OBV values suggest that selling pressure is dominant and may lead to lower prices. Traders use OBV to confirm trends and potential reversals by comparing the OBV line to price movements, with divergences between the two often signaling possible trend changes.

OBV is commonly used in conjunction with other technical indicators to enhance trading decisions and validate trend strength.
"""

def calculate_obv(data):
    """
    Calculate OBV based on the latest two data points
    """
    if len(data) < 2:
        return "Not enough data to calculate OBV"

    latest_data = data[0]
    previous_data = data[1]
    obv = 0

    if latest_data["Close"] > previous_data["Close"]:
        obv += latest_data["Volume"]
    elif latest_data["Close"] < previous_data["Close"]:
        obv -= latest_data["Volume"]

    return obv

async def calculate_stock_obv(function_arguments):
    """
    Calculate OBV for a given stock symbol
    """
    try:
        logger.info("Calculating OBV... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]

        logger.info("Calculating OBV for stock: %s", stock_symbol)

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate OBV
        obv_values = calculate_obv(stock_data)

        logger.info("OBV calculated successfully for stock: %s", stock_symbol)
        return {
            "obvValues": obv_values,
            "description": DESCRIPTION
        }

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating OBV: %s", str(e))
        raise Exception(f"Error calculating OBV: {str(e)}")