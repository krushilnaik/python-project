"""
Unit tests for the Summary model
"""
from datetime import datetime

import pytest

from models.summary import Summary, SummaryValidator


def test_new_summary():
    """
    GIVEN a Summary model
    WHEN a new Summary is created
    THEN check all the fields are defined correctly
    """
    data = {
        "time_period": datetime.strptime('2015-02-21', "%Y-%m-%d"),
        "calls_offered": 2153,
        "abandoned_after_30": 0.23,
        "fcr": 0.01,
        "dsat": 0.51,
        "csat": 0.1547,
    }

    SummaryValidator(**data)

    summary = Summary(**data)

    assert summary.calls_offered == 2153
    assert summary.fcr == 0.01
    assert summary.csat == 0.1547

    as_dict = {
        "Time Period": 'February 2015',
        "Calls Offered": "2,153",
        "Abandon after 30s": "23.00%",
        "FCR": "1.00%",
        "DSAT": "51.00%",
        "CSAT": "15.47%",
    }

    assert as_dict == summary.as_dict()


def test_invalid_input():
    """
    GIVEN a Summary model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    data = {
        "time_period": '2015-02-21 00:00:00',
        "calls_offered": 2153,
        "abandoned_after_30": 5.23,
        "fcr": 2.01,
        "dsat": 5.51,
        "csat": 1.15,
    }

    with pytest.raises(ValueError):
        SummaryValidator(**data)
