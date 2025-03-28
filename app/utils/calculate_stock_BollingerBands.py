import pandas as pd


def calculate_bollinger_bands(
    data: pd.DataFrame, period: int = 20, multiplier: int = 2
):
    """
    Calculate Bollinger Bands for the given data.

    Args:
        data (pd.DataFrame): Stock data with a 'Close' column.
        period (int): The period for the moving average.
        multiplier (int): The multiplier for standard deviation.

    Returns:
        dict: A dictionary containing moving average, upper band, and lower band.
    """
    if len(data) < period:
        return "Not enough data to calculate Bollinger Bands"

    sma = data["Close"].rolling(window=period).mean()
    std_dev = data["Close"].rolling(window=period).std()
    upper_band = sma + (multiplier * std_dev)
    lower_band = sma - (multiplier * std_dev)

    return {
        "moving_average": sma.iloc[-1],
        "upper_band": upper_band.iloc[-1],
        "lower_band": lower_band.iloc[-1],
    }
