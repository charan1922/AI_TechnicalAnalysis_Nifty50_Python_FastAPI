from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
The Average Directional Index (ADX) provides insights into the strength of a trend. ADX values range from 0 to 100. Values between 0 and 25 indicate a weak or absent trend, while values between 25 and 50 suggest a strong trend. When ADX values fall between 50 and 75, they represent a very strong trend, and values from 75 to 100 indicate an extremely strong trend.

The ADX is typically used in conjunction with the Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI). A crossover where +DI crosses above -DI can signal a potential uptrend, whereas when -DI crosses above +DI, it suggests a potential downtrend. Rising ADX values are indicative of a strengthening trend, regardless of its direction, while falling ADX values suggest that the trend is weakening. This information helps traders to better understand and act on market trends.
"""


def calculate_adx(data, period=14):
    """
    Calculate ADX for given stock data over specified period
    """
    logger.info("Starting ADX calculation for period: %s", period)
    if len(data) < period + 1:
        logger.warning("Not enough data to calculate ADX. Data length: %s", len(data))
        return "Not enough data to calculate ADX"

    tr = []
    plus_dm = []
    minus_dm = []

    # Only consider the most recent period+1 data points
    recent_data = data[: period + 1]

    for i in range(1, len(recent_data)):
        high = recent_data[i]["High"]
        low = recent_data[i]["Low"]
        close = recent_data[i]["Close"]
        prev_close = recent_data[i - 1]["Close"]
        prev_high = recent_data[i - 1]["High"]
        prev_low = recent_data[i - 1]["Low"]

        # Calculate True Range (TR)
        tr.append(max(high - low, abs(high - prev_close), abs(low - prev_close)))

        # Calculate +DM and -DM
        current_plus_dm = (
            high - prev_high
            if (high - prev_high > prev_low - low and high - prev_high > 0)
            else 0
        )
        current_minus_dm = (
            prev_low - low
            if (prev_low - low > high - prev_high and prev_low - low > 0)
            else 0
        )

        plus_dm.append(current_plus_dm)
        minus_dm.append(current_minus_dm)

    logger.debug("TR: %s, +DM: %s, -DM: %s", tr, plus_dm, minus_dm)

    # Smooth the TR, +DM, and -DM (simple sum for initial period)
    smoothed_tr = sum(tr)
    smoothed_plus_dm = sum(plus_dm)
    smoothed_minus_dm = sum(minus_dm)

    # Calculate +DI and -DI
    plus_di = (smoothed_plus_dm / smoothed_tr) * 100 if smoothed_tr != 0 else 0
    minus_di = (smoothed_minus_dm / smoothed_tr) * 100 if smoothed_tr != 0 else 0

    # Calculate DX and ADX
    dx = (
        abs((plus_di - minus_di) / (plus_di + minus_di)) * 100
        if (plus_di + minus_di) != 0
        else 0
    )
    adx = dx  # For this simplified version, ADX equals DX for the initial period

    logger.info("ADX calculation completed. ADX: %s", adx)
    return adx


async def calculate_stock_adx(function_arguments):
    """
    Calculate ADX for a given stock symbol
    """
    try:
        logger.info("Calculating ADX... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]
        period = function_arguments.get("period", 14)

        logger.info(
            "Calculating ADX for stock: %s with period: %s", stock_symbol, period
        )

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate ADX
        adx_value = calculate_adx(stock_data, period)

        logger.info("ADX calculated successfully for stock: %s", stock_symbol)
        return {"adxValue": adx_value, "period": period, "description": DESCRIPTION}

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating ADX: %s", str(e))
        raise Exception(f"Error calculating ADX: {str(e)}")
