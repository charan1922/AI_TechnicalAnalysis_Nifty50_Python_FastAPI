import logging
import sys
from logging.handlers import RotatingFileHandler


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Changed from INFO to DEBUG to capture all log levels
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                "app.log", maxBytes=5 * 1024 * 1024, backupCount=3
            ),  # 5MB log file
        ],
    )

    logging.getLogger("pymongo").setLevel(logging.WARNING)


# This FastAPI route:

# Accepts user input via a POST request.
# Retrieves or initializes a session from MongoDB.
# Appends the user message to the session.
# Sends input to OpenAI’s API (gpt-4o-mini).
# Parses the response and returns it if it’s a basic text reply.
# If the response includes tool calls, it:
# Executes the tool.
# Stores the result as function_call_output.
# Updates the session data.
# Repeats the loop if needed.
