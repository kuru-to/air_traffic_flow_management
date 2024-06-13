from __future__ import annotations

from pydantic import BaseModel

from .flight import Flight
from .sector import Sector
from .time import Time


class EnterEvent(BaseModel):
    flight: Flight
    sector: Sector
    expected_time_over: Time

    @classmethod
    def create(cls, flight: int, sector: str, eto: str) -> EnterEvent:
        result = cls(
            flight=Flight(id_=flight),
            sector=Sector(name=sector),
            expected_time_over=Time.create(eto),
        )
        return result
