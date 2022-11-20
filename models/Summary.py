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

    def as_dict(self):
        """
        Return the Summary object as a dictionary of properly formatted strings

        Returns:
            dict: Dictionary mapping the columns to formatted values
        """
        return {
            "Calls Offered": f"{int(self.calls_offered):,}",
            "Abandon after 30s": f'{float(self.abandoned_after_30):.2%}',
            "FCR": f'{float(self.fcr):.2%}',
            "DSAT": f'{float(self.dsat):.2%}',
            "CSAT": f'{float(self.csat):.2%}',
        }
