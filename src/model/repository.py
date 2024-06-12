import abc

from .enter_event import EnterEvent
from .period import Period
from .sector import Sector


class IRepository(abc.ABC):
    @abc.abstractmethod
    def read_sectors(self) -> list[Sector]:
        pass

    @abc.abstractmethod
    def read_periods(self) -> list[Period]:
        pass

    @abc.abstractmethod
    def read_enter_events(self) -> list[EnterEvent]:
        pass
