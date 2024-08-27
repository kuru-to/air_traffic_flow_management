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
        start_hour: int,
        start_minute: int,
        start_second: int,
        end_hour: int,
        end_minute: int,
        end_second: int,
        rate: int,
    ) -> Period:
        result = cls(
            sector=Sector(name=sector_name),
            start=Time.create(start_hour, start_minute, start_second),
            end=Time.create(end_hour, end_minute, end_second),
            rate=rate,
        )
        return result

    def in_period(self, time_: Time) -> bool:
        """period の期間内に入っているか"""
        return self.start <= time_ and time_ <= self.end
