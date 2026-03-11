import logging
from functools import wraps

log_path: str = "logs/log.log"
log_format: str = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(
    filename=log_path,
    format=log_format,
    filemode="w",
    level=logging.INFO)

# Initialize logger
logger = logging.getLogger(__name__)
formatter = logging.Formatter(log_format)
logger.addHandler(logging.FileHandler(log_path))
logger.handlers[0].setFormatter(formatter)

# pass logger to decorator
def log_execution(func1):
    """Decorator function to log when a function starts & terminates"""
    @wraps(func1)
    def wrapper(*args, **kwargs):
        "Decorator wrapper"
        logger.info(f"Running {func1.__name__}")
        func1(*args, **kwargs)
        logger.info(f"Finished {func1.__name__}")
    return wrapper