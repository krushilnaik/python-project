"""
Set up logger
"""

import logging


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
