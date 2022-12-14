"""
Utility functions used throughout the project
"""

import os

from flask import flash

from utils.constants import (ARCHIVE, ERROR, MONTHS, PROCESSED, UPLOADS,
                             VALID_SHEETS)
from utils.logger import error, info


def init_storage():
    """
    Create storage directories if they don't exist
    """

    for _dir in [UPLOADS, ARCHIVE, ERROR]:
        _dir.mkdir(parents=True, exist_ok=True)

    info("Created storage directories")


def clear_file(filename):
    """
    Clear a file's contents

    Args:
        filename (str): _description_
    """

    with open(filename, 'w', encoding="utf-8"):
        pass


def has_required_sheets(sheetnames):
    """
    Make sure all required sheets are present

    Args:
        sheetnames (list): list of sheetnames pulled from openpyxl
    """
    for sheet in VALID_SHEETS:
        if sheet not in sheetnames:
            return False

    return True


def get_month_year(filename):
    """
    Attempt to extract month and year from filename

    Args:
        filename (str): filename

    Raises:
        ValueError: if extraction failed

    Returns:
        tuple: (month, year) <- both numbers
    """

    parts = filename.split("_")[-2:]
    month = MONTHS[parts[0].lower()[:3]]
    year = parts[1][:4]

    if not year.isnumeric():
        raise ValueError("Year could not be inferred from file name")

    return (month, year)


def has_been_parsed(filename):
    """
    Check if a file has already been parsed
    NOTE: this will mark it as parsed if it hasn't

    Args:
        filename (str): filename
    """

    with open(PROCESSED, 'a+', encoding="utf-8") as processed:
        # jump to the start of the file to begin reading
        processed.seek(0)

        if filename in processed.read():
            flash(f"{filename} has already been processed")
            info(f"{filename} has already been processed")
            return True

        info(f"Starting to process {filename}")
        processed.write(filename + "\n")

        return False


def file_to_archives(filename):
    """
    Move a file from uploads folder to archive folder

    Args:
        filename (str): file to move
    """
    info(f"Finished processing {filename}.")
    os.replace(UPLOADS / filename, ARCHIVE / filename)
    info(f"Moved {filename} from 'uploads' to 'archive'")


def file_to_errors(filename, err):
    """
    Move a file from uploads folder to archive folder

    Args:
        filename (str): file to move
    """

    error(err)
    os.replace(UPLOADS / filename, ERROR / filename)
    info(f"Moved {filename} from 'uploads' to 'error'")


def char_range(start, stop):
    """
    Return a list of letters from start to stop

    Args:
        start (char): start char
        stop (char): stop char

    Returns:
        list: list of chars
    """
    return [chr(n) for n in range(ord(start), ord(stop) + 1)]
