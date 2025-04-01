from app.core.database import get_database
from app.core.logger import logging

logger = logging.getLogger(__name__)


async def get_nifty_stock_symbol_info(stock_name):
    logger.info("Fetching Nifty stock symbol info for: %s", stock_name)
    db = get_database()
    collection = db["nifty50"]

    # Create a case-insensitive regex pattern for partial matching
    regex = {"$regex": stock_name, "$options": "i"}

    try:
        stock = collection.find_one(
            {"$or": [{"Symbol": regex}, {"Company Name": regex}]}
        )
        if stock:
            logger.info("Stock found: %s", stock)
            return stock
        else:
            logger.warning("Stock not found for: %s", stock_name)
            return f"Stock not found: {stock_name}. Please try again."
    except Exception as e:
        logger.error("Error fetching stock symbol info: %s", str(e))
        raise e


async def get_stocks_by_industry(industry):
    logger.info("Fetching stocks for industry: %s", industry)
    db = get_database()
    collection = db["nifty50"]

    # Create a case-insensitive regex pattern for partial matching
    regex = {"$regex": industry, "$options": "i"}

    try:
        stock_list = collection.find({"Industry": regex}).to_list(length=None)
        if stock_list:
            logger.info("Stocks found for industry %s: %d", industry, len(stock_list))
            return stock_list
        else:
            logger.warning("No stocks found for industry: %s", industry)
            return f"Stock List not found for {industry} Industry. Please try again."
    except Exception as e:
        logger.error("Error fetching stocks by industry: %s", str(e))
        raise e


async def get_stock_price(stock_symbol):
    logger.info("Fetching stock price for symbol: %s", stock_symbol)
    try:
        db = get_database()
        collection = db[stock_symbol]

        stock_data = collection.find({}).sort("Date", -1).limit(1).to_list(length=1)
        latest_stock_price = None
        if stock_data:
            latest_stock_price = stock_data[0]["Close"]
            logger.info(
                "Latest stock price for %s: %s", stock_symbol, latest_stock_price
            )
        else:
            logger.warning("No stock data found for symbol: %s", stock_symbol)

        return {"symbol": stock_symbol, "price": latest_stock_price}
    except Exception as error:
        logger.error("Error fetching stock price for %s: %s", stock_symbol, error)
        raise error


async def stock_collection(stock_symbol):
    logger.info("Retrieving collection for stock symbol: %s", stock_symbol)
    db = get_database()
    collection = db[stock_symbol]
    try:
        return collection
    except Exception as e:
        logger.error("Error retrieving collection for %s: %s", stock_symbol, str(e))
        raise e
