import pandas as pd


def calculate_stochastic_oscillator(data: pd.DataFrame, period: int = 14):
    """
    Calculate the Stochastic Oscillator for the given data.

    Args:
        data (pd.DataFrame): Stock data with 'High', 'Low', and 'Close' columns.
        period (int): The period for the calculation.

    Returns:
        float: The %K value of the Stochastic Oscillator.
    """
    if len(data) < period:
        return "Not enough data to calculate Stochastic Oscillator"

    highest_high = data["High"].rolling(window=period).max()
    lowest_low = data["Low"].rolling(window=period).min()
    percent_k = ((data["Close"] - lowest_low) / (highest_high - lowest_low)) * 100
    return percent_k.iloc[-1]
