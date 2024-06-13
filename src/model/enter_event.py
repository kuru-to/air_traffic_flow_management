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
    def create(cls, flight_num: int, sector_name: str, expected_time_over: str) -> EnterEvent:
        result = cls(
            flight=Flight(id_=flight_num),
            sector=Sector(name=sector_name),
            expected_time_over=Time.create(expected_time_over),
        )
        return result
