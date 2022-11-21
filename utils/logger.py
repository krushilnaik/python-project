"""
Custom logging module to use throughout the application
"""
import logging

logger = logging.getLogger('file_logger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')

file_handler = logging.FileHandler('flask_app.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


def info(message):
    """
    Log an info message to flask_app.log
    """
    return logger.info(message)


def error(message):
    """
    Log an error message to flask_app.log
    """
    return logger.error(message)
