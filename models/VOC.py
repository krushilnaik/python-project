"""
Representation of the 'voc' MySQL table
"""

from . import db


class VOC(db.Model):
    """
    Representation of the 'voc' MySQL table
    """
    id = db.Column(db.Integer, primary_key=True)
    time_period = db.Column(db.Date)
