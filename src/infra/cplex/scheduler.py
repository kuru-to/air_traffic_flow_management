from docplex.cp.solution import CpoModelSolution

from ...model.air_traffic_flow import AirTrafficFlow
from ...model.air_traffic_flow_scheduler.input import AirTrafficFlowSchedulerInput
from ...model.air_traffic_flow_scheduler.output import AirTrafficFlowSchedulerOutput
from ...model.air_traffic_flow_scheduler.parameters import (
    AirTrafficFlowSchedulerParameters,
)
from ...model.air_traffic_flow_scheduler.scheduler import IAirTrafficFlowScheduler
from ...model.time import Time
from .scheduling_model_builder import IAirTrafficFlowSchedulingModelBuilder


class AirTrafficFlowScheduler(IAirTrafficFlowScheduler):
    """Air traffic flow についてスケジューリングを行う"""

    model_builder: IAirTrafficFlowSchedulingModelBuilder

    def __init__(self, model_builder: IAirTrafficFlowSchedulingModelBuilder):
        self.model_builder = model_builder

    def run(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ) -> AirTrafficFlowSchedulerOutput:
        model = self.model_builder.build(input_, parameters)
        solution: CpoModelSolution = model.solve()

        if not solution.is_solution():
            return self.create_empty_output(input_)

        air_traffic_flows: list[AirTrafficFlow] = []
        for i, enter_event in enumerate(input_.enter_events):
            var_sol = solution.get_var_solution(f"interval_event_{i}")
            enter_slot = var_sol.get_start()
            elapsed_minutes = enter_slot * parameters.time_step
            enter_time = Time(hours=elapsed_minutes // 60, minutes=elapsed_minutes % 60, seconds=0)

            air_traffic_flows.append(
                AirTrafficFlow(flight=enter_event.flight, sector=enter_event.sector, enter_time=enter_time)
            )

        return AirTrafficFlowSchedulerOutput(input_=input_, is_feasible=True, air_traffic_flows=air_traffic_flows)
