from __future__ import annotations

from pydantic import BaseModel, Field, computed_field, field_serializer

from .enter_event import EnterEvent
from .flight import Flight
from .sector import Sector
from .time import Time


class AirTrafficFlow(BaseModel):
    """スケジューリングによって作成される, どのフライトがどの区画に何時に進入するかを表すクラス"""

    flight: Flight
    sector: Sector
    # Time型は書き込みする際に hour, minute, second で列を分けるため, enter_time 自体は書き込みの対象とならない
    enter_time: Time = Field(exclude=True)

    @classmethod
    def create(cls, flight: int, sector: str, enter_hour: int, enter_minute: int, enter_second: int) -> AirTrafficFlow:
        result = cls(
            flight=Flight(id_=flight),
            sector=Sector(name=sector),
            enter_time=Time.create(enter_hour, enter_minute, enter_second),
        )
        return result

    @computed_field
    @property
    def enter_hour(self) -> int:
        return self.enter_time.hours

    @computed_field
    @property
    def enter_minute(self) -> int:
        return self.enter_time.minutes

    @computed_field
    @property
    def enter_second(self) -> int:
        return self.enter_time.seconds

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

    @classmethod
    def to_header(cls) -> list[str]:
        return "flight,sector,enter_hour,enter_minute,enter_second".split(",")
