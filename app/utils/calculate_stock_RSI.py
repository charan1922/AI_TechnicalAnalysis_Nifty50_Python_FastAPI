import pandas as pd


def calculate_rsi(data: pd.DataFrame, period: int = 14):
    """
    Calculate the Relative Strength Index (RSI) for the given data.

    Args:
        data (pd.DataFrame): Stock data with a 'Close' column.
        period (int): The period for RSI calculation.

    Returns:
        float: The calculated RSI.
    """
    if len(data) < period:
        return "Not enough data points to calculate RSI"

    delta = data["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]
