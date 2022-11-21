"""
Utility functions used throughout the project
"""

import os

from flask import flash

from models import db
from models.summary import Summary, SummaryValidator
from utils.constants import ARCHIVE, ERROR, MONTHS, UPLOADS, VALID_SHEETS
from utils.logger import error, info


def init_storage():
    """
    Create storage directories if they don't exist
    """

    for _dir in [UPLOADS, ARCHIVE, ERROR]:
        _dir.mkdir(parents=True, exist_ok=True)

    info("Created storage directories")


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

    with open('processed.lst', 'a+', encoding="utf-8") as processed:
        # jump to the start of the file to begin reading
        processed.seek(0)

        if filename in processed.read():
            flash(f"{filename} has already been processed")
            info(f"{filename} has already been processed")
            return True

        info(f"Starting to process {filename}")
        processed.write(filename + "\n")

        return False


def validate_and_write(values: list):
    """
    Write data to MySQL upon successful validation

    Args:
        values (list): [time_period, calls_offered, abandoned_after_30, fcr, dsat, csat]
    """

    # run each row through the validator
    SummaryValidator(
        time_period=values[0],
        calls_offered=values[1],
        abandoned_after_30=values[2],
        fcr=values[3],
        dsat=values[4],
        csat=values[5]
    )

    # load validated data into ORM
    row = Summary(
        time_period=values[0],
        calls_offered=values[1],
        abandoned_after_30=values[2],
        fcr=values[3],
        dsat=values[4],
        csat=values[5],
    )

    # write row to mysql
    db.session.add(row)
    db.session.commit()

    return row.as_dict()


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
