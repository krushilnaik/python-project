from . import db


class Summary(db.Model):
    """
    Representation of the 'summary' MySQL table
    """

    __tablename__ = "summary"

    id = db.Column(db.Integer, primary_key=True)
    time_period = db.Column(db.Date)
    calls_offered = db.Column(db.String(8))
    abandoned_after_30 = db.Column(db.String(7))
    fcr = db.Column(db.String(7))
    dsat = db.Column(db.String(7))
    csat = db.Column(db.String(7))
