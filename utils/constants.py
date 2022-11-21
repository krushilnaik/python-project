"""
Collection of constants used throughout the project
"""

from pathlib import Path

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

SUMMARY_SHEET = "Summary Rolling MoM"
VOC_SHEET = "VOC Rolling MoM"
VERBATIM_SHEET = "Monthly Verbatim Statements"

VALID_SHEETS = set([
    SUMMARY_SHEET,
    VOC_SHEET,
    VERBATIM_SHEET
])

UPLOADS = Path('./uploads')
ARCHIVE = Path('./archive')
ERROR = Path('./error')
