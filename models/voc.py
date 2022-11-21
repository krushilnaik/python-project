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
    promoters = db.Column(db.Integer)
    passives = db.Column(db.Integer)
    detractors = db.Column(db.Integer)

    @classmethod
    def get_entry(cls, year, month):
        """
        Search database for entry by year and month

        Args:
            year (int): year
            month (int): month

        Returns:
            VOC: entry
        """

        return cls.query.filter(VOC.time_period.between(
            f'{year}-{month}-01', f'{year}-{month}-31')
        ).first()

    def save(self):
        """
        Validate and write this row to database
        """
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        """
        Return the VOC object as a dictionary

        Returns:
            dict:
        """

        return {
            "promoters": self.promoters,
            "passives": self.passives,
            "detractors": self.detractors
        }


# class VOCValidator(BaseModel):
#     """
#     Helper class to validate data before being entered into the database

#     Raises:
#         ValidationError: in the event one of the fields failed validation
#     """
