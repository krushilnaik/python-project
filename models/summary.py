"""
Representation of the 'summary' MySQL table
"""

from datetime import datetime

from pydantic import BaseModel, validator

from . import db


class Summary(db.Model):
    """
    Representation of the 'summary' MySQL table
    """

    __tablename__ = "summary"

    id = db.Column(db.Integer, primary_key=True)
    time_period = db.Column(db.Date)
    calls_offered = db.Column(db.Integer)
    abandoned_after_30 = db.Column(db.Float)
    fcr = db.Column(db.Float)
    dsat = db.Column(db.Float)
    csat = db.Column(db.Float)

    @classmethod
    def get_entry(cls, year, month):
        """
        Search database for entry by year and month

        Args:
            year (int): year
            month (int): month

        Returns:
            Summary: entry
        """
        return cls.query.filter(Summary.time_period.between(
            f'{year}-{month}-01', f'{year}-{month}-31')
        ).first()

    def as_dict(self):
        """
        Return the Summary object as a dictionary of properly formatted strings

        Returns:
            dict: Dictionary mapping the columns to formatted values
        """

        return {
            "Time Period": f"{self.time_period:%B %Y}",
            "Calls Offered": f"{self.calls_offered:,}",
            "Abandon after 30s": f'{self.abandoned_after_30:.2%}',
            "FCR": f'{self.fcr:.2%}',
            "DSAT": f'{self.dsat:.2%}',
            "CSAT": f'{self.csat:.2%}',
        }


class SummaryValidator(BaseModel):
    """
    Helper class to validate data before being entered into the database

    Raises:
        ValidationError: in the event one of the fields failed validation
    """

    time_period: datetime
    calls_offered: int
    abandoned_after_30: float
    fcr: float
    dsat: float
    csat: float

    @validator("abandoned_after_30", "fcr", "dsat", "csat")
    def less_than_one(cls, value):
        """
        Percentages are stored in the database as a floating point betweeo 0 and 1.
        Make sure the data matches those constraints.

        Raises:
            ValidationError:

        Returns:
            _type_: _description_
        """

        try:
            if float(value) > 1.0:
                raise ValueError("Percentages must be less than 1.0")

            return float(value)
        except ValueError as error:
            raise error
