from pydantic import BaseModel, model_validator

from ..enter_event import EnterEvent
from ..flight import Flight
from ..period import Period
from ..sector import Sector


class AirTrafficFlowSchedulerInput(BaseModel):
    sectors: list[Sector]
    periods: list[Period]
    enter_events: list[EnterEvent]

    @model_validator(mode="after")
    def validate_existing_sector(self):
        for p in self.periods:
            if p.sector not in set(self.sectors):
                raise ValueError(f"Period's sector({p.sector}) does not exist in sectors: {self.sectors}.")

        for e in self.enter_events:
            if e.sector not in set(self.sectors):
                raise ValueError(f"EnterEvent's sector({p.sector}) does not exist in sectors: {self.sectors}.")

        return self

    @property
    def num_sectors(self) -> int:
        return len(self.sectors)

    @property
    def num_enters(self) -> int:
        return len(self.enter_events)

    @property
    def flights(self) -> list[Flight]:
        return list({e.flight for e in self.enter_events})

    def periods_by_sector(self, query_sector: Sector) -> list[Period]:
        return [p for p in self.periods if p.sector == query_sector]
