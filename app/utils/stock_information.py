from app.core.database import get_database


async def get_nifty_stock_symbol_info(stock_name):
    db = get_database()
    collection = db["nifty50"]

    # Create a case-insensitive regex pattern for partial matching
    regex = {"$regex": stock_name, "$options": "i"}

    # Find the stock by partial matching Symbol or Company Name
    stock = collection.find_one({"$or": [{"Symbol": regex}, {"Company Name": regex}]})

    if stock:
        return stock
    else:
        return f"Stock not found: {stock_name}. Please try again."


async def get_stocks_by_industry(industry):
    """
    Retrieves a list of stocks in a specific industry from the Nifty50 collection.

    :param industry: The industry name to search for
    :return: A list of stocks in the specified industry, or an error message if not found
    """
    db = get_database()
    collection = db["nifty50"]

    # Create a case-insensitive regex pattern for partial matching
    regex = {"$regex": industry, "$options": "i"}

    # Find the stock list by partial matching Industry
    stock_list = collection.find({"Industry": regex}).to_list(length=None)

    if stock_list:
        return stock_list
    else:
        return f"Stock List not found for {industry} Industry. Please try again."


async def get_stock_price(stock_symbol):
    """
    Retrieves the latest stock price for a given stock symbol.

    :param stock_symbol: The stock symbol to search for
    :return: A dictionary containing the stock symbol and its latest price
    """
    try:
        db = get_database()  # Ensure get_database is awaited if it is async
        collection = db[stock_symbol]

        # Fetch the latest stock price by sorting by Date in descending order
        stock_data = collection.find({}).sort("Date", -1).limit(1).to_list(length=1)

        latest_stock_price = None
        if stock_data:
            latest_stock_price = stock_data[0]["Close"]

        return {"symbol": stock_symbol, "price": latest_stock_price}
    except Exception as error:
        print(f"Error fetching stock price for {stock_symbol}: {error}")
        raise error
