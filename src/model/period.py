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
        start_time: dict[str, int],
        end_time: dict[str, int],
        rate: int,
    ) -> Period:
        result = cls(
            sector=Sector(name=sector_name),
            start=Time(**start_time),
            end=Time(**end_time),
            rate=rate,
        )
        return result
