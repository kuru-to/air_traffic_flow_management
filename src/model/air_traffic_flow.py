from __future__ import annotations

from pydantic import BaseModel

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
    def create(
        cls, flight_num: int, sector_name: str, enter_time: dict[str, int]
    ) -> AirTrafficFlow:
        result = cls(
            Flight(id_=flight_num), Sector(name=sector_name), Time(**enter_time)
        )
        return result

    def delay(self, enter_event: EnterEvent) -> int:
        """対応する進入イベントに対し, どれだけ遅れが生じたか"""
        if self.flight != enter_event.flight or self.sector != enter_event.sector:
            return 0
        return max(0, self.enter_time - enter_event.expected_time_over)
