"""
Set up logger
"""

import logging


file_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [@%(filename)s:%(lineno)d]'
)

logging.basicConfig(filename='flask_app.log',
                    encoding='utf-8', level=logging.DEBUG)


def info(message):
    """
    Write info message to logger

    Args:
        message (str): message
    """
    logging.info(message)


def error(message):
    """
    Write error message to logger

    Args:
        message (str): message
    """
    logging.error(message)
