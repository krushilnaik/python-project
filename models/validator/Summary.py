from pydantic import BaseModel, validator, ValidationError
from datetime import datetime


class Summary(BaseModel):
    id: int
    time_period: datetime
    calls_offered: int
    abandoned_after_30 = float
    fcr = float
    dsat = float
    csat = float

    @validator("abandoned_after_30", "fcr", "dsat", "csat")
    def less_than_one(cls, value):
        if value > 1:
            raise ValidationError("Percentages must be less than 100%")

        return value
