from app.utils.stock_information import stock_collection
from app.core.logger import logging

logger = logging.getLogger(__name__)

# Description constant
DESCRIPTION = """
The Ichimoku Cloud, also known as Ichimoku Kinko Hyo, is a comprehensive technical indicator that provides insights into support and resistance levels, trend direction, and momentum. It consists of five lines plotted on a price chart, creating a 'cloud' that helps traders analyze the market at a glance.

The five lines are:
1. **Tenkan-sen (Conversion Line):** Calculated as the average of the highest high and the lowest low over the past 9 periods.
2. **Kijun-sen (Base Line):** Calculated as the average of the highest high and the lowest low over the past 26 periods.
3. **Senkou Span A (Leading Span A):** Calculated as the average of the Tenkan-sen and Kijun-sen, plotted 26 periods ahead.
4. **Senkou Span B (Leading Span B):** Calculated as the average of the highest high and the lowest low over the past 52 periods, plotted 26 periods ahead.
5. **Chikou Span (Lagging Span):** The current closing price plotted 26 periods behind.

The area between Senkou Span A and Senkou Span B forms the 'cloud,' which acts as support or resistance. A price above the cloud suggests a bullish trend, while a price below the cloud indicates a bearish trend. When the cloud is thick, it signals strong support or resistance, and when it is thin, it signals weaker support or resistance. The Ichimoku Cloud helps traders identify trend strength, potential reversal points, and overall market sentiment.
"""


def calculate_ichimoku_cloud(data):
    """
    Calculate Ichimoku Cloud components for given stock data
    """
    if len(data) < 52:
        return "Not enough data to calculate Ichimoku Cloud"

    def get_high_low(data_subset, period):
        """Helper function to calculate highest high and lowest low over a period"""
        highs = [item["High"] for item in data_subset[:period]]
        lows = [item["Low"] for item in data_subset[:period]]
        return {"highestHigh": max(highs), "lowestLow": min(lows)}

    # Calculate Tenkan-sen (Conversion Line) - 9 periods
    tenkan_period = 9
    tenkan_high_low = get_high_low(data, tenkan_period)
    tenkan_sen = (tenkan_high_low["highestHigh"] + tenkan_high_low["lowestLow"]) / 2

    # Calculate Kijun-sen (Base Line) - 26 periods
    kijun_period = 26
    kijun_high_low = get_high_low(data, kijun_period)
    kijun_sen = (kijun_high_low["highestHigh"] + kijun_high_low["lowestLow"]) / 2

    # Calculate Senkou Span A (Leading Span A)
    senkou_span_a = (tenkan_sen + kijun_sen) / 2

    # Calculate Senkou Span B (Leading Span B) - 52 periods
    senkou_period = 52
    senkou_high_low = get_high_low(data, senkou_period)
    senkou_span_b = (senkou_high_low["highestHigh"] + senkou_high_low["lowestLow"]) / 2

    # Calculate Chikou Span (Lagging Span) - current closing price
    chikou_span = data[0]["Close"]

    return {
        "tenkanSen": tenkan_sen,
        "kijunSen": kijun_sen,
        "senkouSpanA": senkou_span_a,
        "senkouSpanB": senkou_span_b,
        "chikouSpan": chikou_span,
    }


async def calculate_stock_ichimoku_cloud(function_arguments):
    """
    Calculate Ichimoku Cloud for a given stock symbol
    """
    try:
        logger.info("Calculating Ichimoku Cloud... %s", function_arguments)
        stock_symbol = function_arguments["stockSymbol"]

        logger.info("Calculating Ichimoku Cloud for stock: %s", stock_symbol)

        # Get stock collection
        collection = await stock_collection(stock_symbol)
        logger.info("Collection for stock %s: %s", stock_symbol, collection.name)

        # Get stock data sorted by date in descending order
        stock_data = list(collection.find().sort("Date", -1))

        # Calculate Ichimoku Cloud
        ichimoku_cloud = calculate_ichimoku_cloud(stock_data)

        logger.info(
            "Ichimoku Cloud calculated successfully for stock: %s", stock_symbol
        )
        return {"ichimokuCloud": ichimoku_cloud, "description": DESCRIPTION}

    except KeyError as e:
        logger.error("Missing key in function_arguments: %s", str(e))
        raise Exception(f"Missing key in function_arguments: {str(e)}")
    except Exception as e:
        logger.error("Error calculating Ichimoku Cloud: %s", str(e))
        raise Exception(f"Error calculating Ichimoku Cloud: {str(e)}")
