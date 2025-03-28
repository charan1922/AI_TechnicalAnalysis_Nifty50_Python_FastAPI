import pandas as pd


def calculate_vwap(data: pd.DataFrame):
    """
    Calculate the Volume Weighted Average Price (VWAP) for the given data.

    Args:
        data (pd.DataFrame): Stock data with 'High', 'Low', 'Close', and 'Volume' columns.

    Returns:
        float: The calculated VWAP.
    """
    if len(data) == 0:
        return "Not enough data to calculate VWAP"

    typical_price = (data["High"] + data["Low"] + data["Close"]) / 3
    vwap = (typical_price * data["Volume"]).sum() / data["Volume"].sum()
    return vwap
