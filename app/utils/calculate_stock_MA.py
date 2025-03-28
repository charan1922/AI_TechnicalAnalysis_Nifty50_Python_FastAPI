import pandas as pd


def calculate_moving_average(data: pd.DataFrame, period: int = 50):
    """
    Calculate the Moving Average (MA) for the given data.

    Args:
        data (pd.DataFrame): Stock data with a 'Close' column.
        period (int): The period for the moving average.

    Returns:
        float: The calculated moving average.
    """
    if len(data) < period:
        return "Not enough data"
    return data["Close"].rolling(window=period).mean().iloc[-1]
