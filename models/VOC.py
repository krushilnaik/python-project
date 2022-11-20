from . import db


class VOC(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_period = db.Column(db.Date)
