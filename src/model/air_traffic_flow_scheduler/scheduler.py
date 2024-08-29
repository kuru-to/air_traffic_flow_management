import abc

from ...logger.logger import get_main_logger, indent
from .input import AirTrafficFlowSchedulerInput
from .output import AirTrafficFlowSchedulerOutput
from .parameters import AirTrafficFlowSchedulerParameters

logger = get_main_logger()


class IAirTrafficFlowScheduler(abc.ABC):
    """Air traffic flow についてスケジューリングを行う
    CPLEX を使ってスケジューリングするとは限らないので, インターフェースとする"""

    def create_empty_output(self, input_: AirTrafficFlowSchedulerInput) -> AirTrafficFlowSchedulerOutput:
        return AirTrafficFlowSchedulerOutput(input_=input_, is_feasible=False, air_traffic_flows=[])

    def log_journey_by_flight(self, output: AirTrafficFlowSchedulerOutput):
        """各フライトでどのような旅路をたどったのかを logging

        Args:
            output (AirTrafficFlowSchedulerOutput): 出力結果
        """
        for f in output.input_.flights:
            logger.info(f"flight: {f.id_}")
            air_traffic_flow_by_flight = sorted(
                [a for a in output.air_traffic_flows if a.flight == f], key=lambda x: x.enter_time
            )
            for a in air_traffic_flow_by_flight:
                enter_event = [e for e in output.input_.enter_events if e.flight == f and e.sector == a.sector][0]
                logger.info(
                    f"{indent}enter {a.sector}, time: {a.enter_time}, expected_time_over: {enter_event.expected_time_over}"
                )

                delay_seconds = a.delay(enter_event)
                if delay_seconds > 0:
                    logger.info(f"{indent*2}delay occured! delay minutes: {delay_seconds // 60}")

    @abc.abstractmethod
    def run(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ) -> AirTrafficFlowSchedulerOutput:
        pass
