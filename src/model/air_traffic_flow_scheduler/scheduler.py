import abc

from .input import AirTrafficFlowSchedulerInput
from .output import AirTrafficFlowSchedulerOutput
from .parameters import AirTrafficFlowSchedulerParameters


class IAirTrafficFlowScheduler(abc.ABC):
    """Air traffic flow についてスケジューリングを行う
    CPLEX を使ってスケジューリングするとは限らないので, インターフェースとする"""

    def create_empty_output(self, input_: AirTrafficFlowSchedulerInput) -> AirTrafficFlowSchedulerOutput:
        return AirTrafficFlowSchedulerOutput(input_=input_, is_feasible=False, air_traffic_flows=[])

    @abc.abstractmethod
    def run(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ) -> AirTrafficFlowSchedulerOutput:
        pass
