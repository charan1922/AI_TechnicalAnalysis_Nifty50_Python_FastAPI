import yfinance as yf
from datetime import datetime, timedelta


def download_historical_data(stock_symbol: str, filename: str):
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

        if stock_data.empty:
            print(f"No data found for {stock_symbol}.")
            return

        stock_data.to_csv(filename)
        print(f"Data successfully downloaded to {filename}")

    except Exception as e:
        print(f"Error downloading historical data: {e}")


if __name__ == "__main__":
    stock_symbol = "TCS.NS"
    filename = "TCS_historical_data.csv"
    download_historical_data(stock_symbol, filename)
