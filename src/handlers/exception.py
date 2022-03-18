import logging


def exception_handler(func):
    def inner_function(*args, **kwargs):
        logger = logging.getLogger(__name__)
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error(f"{func.__name__}> {str(e)}")

    return inner_function
