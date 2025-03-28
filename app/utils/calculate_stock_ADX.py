import pandas as pd


def calculate_adx(data: pd.DataFrame, period: int = 14):
    """
    Calculate the Average Directional Index (ADX) for the given data.

    Args:
        data (pd.DataFrame): Stock data with 'High', 'Low', and 'Close' columns.
        period (int): The period for the ADX calculation.

    Returns:
        float: The calculated ADX value.
    """
    if len(data) < period + 1:
        return "Not enough data to calculate ADX"

    tr = []
    plus_dm = []
    minus_dm = []

    for i in range(1, len(data)):
        high = data["High"].iloc[i]
        low = data["Low"].iloc[i]
        prev_close = data["Close"].iloc[i - 1]
        prev_high = data["High"].iloc[i - 1]
        prev_low = data["Low"].iloc[i - 1]

        tr.append(max(high - low, abs(high - prev_close), abs(low - prev_close)))
        plus_dm.append(
            max(high - prev_high, 0) if high - prev_high > prev_low - low else 0
        )
        minus_dm.append(
            max(prev_low - low, 0) if prev_low - low > high - prev_high else 0
        )

    tr_smooth = pd.Series(tr).rolling(window=period).mean()
    plus_dm_smooth = pd.Series(plus_dm).rolling(window=period).mean()
    minus_dm_smooth = pd.Series(minus_dm).rolling(window=period).mean()

    plus_di = (plus_dm_smooth / tr_smooth) * 100
    minus_di = (minus_dm_smooth / tr_smooth) * 100
    dx = (abs(plus_di - minus_di) / (plus_di + minus_di)) * 100
    adx = dx.rolling(window=period).mean()

    return adx.iloc[-1]
