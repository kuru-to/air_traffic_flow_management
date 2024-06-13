from __future__ import annotations

from pydantic import BaseModel, Field, model_validator

from .sector import Sector
from .time import Time


class Period(BaseModel):
    sector: Sector
    start: Time
    end: Time
    rate: int = Field(..., ge=0, le=100)

    @model_validator(mode="after")
    def validate_start_before_end(self):
        if self.start > self.end:
            raise ValueError("Period must start before end.")
        return self

    @classmethod
    def create(
        cls,
        sector_name: str,
        start_time: str,
        end_time: str,
        rate: int,
    ) -> Period:
        result = cls(
            sector=Sector(name=sector_name),
            start=Time.create(start_time),
            end=Time.create(end_time),
            rate=rate,
        )
        return result
