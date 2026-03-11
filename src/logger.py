import logging
from functools import wraps

from .config import get_configs

log_str_to_obj: dict = {
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# Retrieve log path & format from config file, or use defaults
configs: dict = get_configs()
log_path: str = configs.get("log_path", "logs/log.log")
log_format: str = configs.get("log_format", "%(asctime)s | %(levelname)s | %(message)s")
logging_level: int = log_str_to_obj.get(configs.get("logging_level", "INFO"), logging.INFO)

logging.basicConfig(
    filename=log_path,
    format=log_format,
    filemode="w",
    level=logging_level)

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