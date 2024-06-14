from __future__ import annotations

from pydantic import BaseModel, field_serializer

from .enter_event import EnterEvent
from .flight import Flight
from .sector import Sector
from .time import Time


class AirTrafficFlow(BaseModel):
    """スケジューリングによって作成される, どのフライトがどの区画に何時に進入するかを表すクラス"""

    flight: Flight
    sector: Sector
    enter_time: Time

    @classmethod
    def create(cls, flight: int, sector: str, enter_time: str) -> AirTrafficFlow:
        result = cls(flight=Flight(id_=flight), sector=Sector(name=sector), enter_time=Time.create(enter_time))
        return result

    def delay(self, enter_event: EnterEvent) -> int:
        """対応する進入イベントに対し, どれだけ遅れが生じたか"""
        if self.flight != enter_event.flight or self.sector != enter_event.sector:
            return 0
        return max(0, self.enter_time - enter_event.expected_time_over)

    @field_serializer("flight")
    def serialize_flight_to_str(self, flight: Flight) -> int:
        return flight.id_

    @field_serializer("sector")
    def serialize_sector_to_str(self, sector: Sector) -> str:
        return sector.name

    @field_serializer("enter_time")
    def serialize_enter_time_to_str(self, enter_time: Time) -> str:
        return str(enter_time)
