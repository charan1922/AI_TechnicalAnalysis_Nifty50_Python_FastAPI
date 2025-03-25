import logging
import sys  # Required for sys.stdout in StreamHandler


# Function to configure logging for the application
def configure_logging():
    # Set up basic logging configuration
    logging.basicConfig(
        level=logging.INFO,  # Log level: Captures info-level logs and above
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",  # Log message format
        handlers=[
            logging.StreamHandler(sys.stdout),  # Output logs to the console
            logging.FileHandler(
                "app.log", mode="a"
            ),  # Append logs to a file named 'app.log'
        ],
    )

    # Customize specific loggers if needed
    logging.getLogger("uvicorn").setLevel(
        logging.WARNING
    )  # Set 'uvicorn' logger to warning level
    logging.getLogger("pymongo").setLevel(
        logging.WARNING
    )  # Set 'pymongo' logger to warning level


# Log level explanation:
# level=logging.INFO: Captures info-level logs and above (info, warning, error, critical).

# Structured Format:
# %(asctime)s: Timestamp of the log
# %(name)s: Logger name (module or package)
# %(levelname)s: Severity of the log
# %(message)s: Actual log message

# Handlers:
# Logs are output to both the console (sys.stdout) and a file (app.log).
