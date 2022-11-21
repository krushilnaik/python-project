"""
Representation of the 'voc' MySQL table
"""

# from pydantic import BaseModel

from . import db


class VOC(db.Model):
    """
    Representation of the 'voc' MySQL table
    """
    id = db.Column(db.Integer, primary_key=True)
    time_period = db.Column(db.Date)
    promoters = db.Column(db.Integer)
    passives = db.Column(db.Integer)
    detractors = db.Column(db.Integer)


# class VOCValidator(BaseModel):
#     """
#     Helper class to validate data before being entered into the database

#     Raises:
#         ValidationError: in the event one of the fields failed validation
#     """
