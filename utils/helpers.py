"""
Utility functions
"""

import os

from models import db
from models.summary import Summary, SummaryValidator
from flask import redirect, url_for
from .logger import error, info

from utils.constants import UPLOADS, ARCHIVE, ERROR


def goto(view):
    return redirect(url_for(view))


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
