import logging
from functools import wraps

# pass logger to decorator
def logging(func1):
    # func is available
    @wraps(func1)
    def wrapper(*args, **kwargs):
        """LogWrapper Docstring"""
        logger.warning("logging start")
        func1(*args, **kwargs)
        logger.warning("logging end")
    return wrapper