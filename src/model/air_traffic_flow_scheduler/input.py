from pydantic import BaseModel

from ..enter_event import EnterEvent
from ..flight import Flight
from ..period import Period
from ..sector import Sector


class AirTrafficFlowSchedulerInput(BaseModel):
    sectors: list[Sector]
    periods: list[Period]
    enter_events: list[EnterEvent]

    @property
    def num_enters(self) -> int:
        return len(self.enter_events)

    @property
    def flights(self) -> list[Flight]:
        return list({e.flight for e in self.enter_events})

    def periods_by_sector(self, query_sector: Sector) -> list[Period]:
        return [p for p in self.periods if p.sector == query_sector]
