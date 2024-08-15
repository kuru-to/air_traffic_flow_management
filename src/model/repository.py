import abc

from .air_traffic_flow import AirTrafficFlow
from .enter_event import EnterEvent
from .period import Period


class IRepository(abc.ABC):

    @abc.abstractmethod
    def read_periods(self) -> list[Period]:
        pass

    @abc.abstractmethod
    def read_enter_events(self) -> list[EnterEvent]:
        pass

    @abc.abstractmethod
    def write_air_traffic_flows(self, air_traffic_flows: list[AirTrafficFlow]):
        pass
