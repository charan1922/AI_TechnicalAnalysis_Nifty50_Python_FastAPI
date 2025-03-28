import pandas as pd


def calculate_macd(
    data: pd.DataFrame,
    short_period: int = 12,
    long_period: int = 26,
    signal_period: int = 9,
):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for the given data.

    Args:
        data (pd.DataFrame): Stock data with a 'Close' column.
        short_period (int): The short EMA period.
        long_period (int): The long EMA period.
        signal_period (int): The signal line period.

    Returns:
        dict: A dictionary containing MACD line, signal line, and histogram.
    """
    if len(data) < long_period:
        return "Not enough data to calculate MACD"

    short_ema = data["Close"].ewm(span=short_period, adjust=False).mean()
    long_ema = data["Close"].ewm(span=long_period, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        "macd_line": macd_line.iloc[-1],
        "signal_line": signal_line.iloc[-1],
        "histogram": histogram.iloc[-1],
    }
