from docplex.cp.solution import CpoModelSolution

from ..air_traffic_flow import AirTrafficFlow
from ..time import Time
from .input import AirTrafficFlowSchedulerInput
from .output import AirTrafficFlowSchedulerOutput
from .parameters import AirTrafficFlowSchedulerParameters
from .scheduling_model_builder import IAirTrafficFlowSchedulingModelBuilder


class AirTrafficFlowScheduler:
    """Air traffic flow についてスケジューリングを行う"""

    def run(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
        model_builder: IAirTrafficFlowSchedulingModelBuilder,
    ) -> AirTrafficFlowSchedulerOutput:
        model = model_builder.build(input_, parameters)
        solution: CpoModelSolution = model.solve()

        if not solution.is_solution():
            return AirTrafficFlowSchedulerOutput(input_=input_, is_feasible=False, air_traffic_flows=[])

        air_traffic_flows: list[AirTrafficFlow] = []
        for i, enter_event in enumerate(input_.enter_events):
            var_sol = solution.get_var_solution(f"interval_event_{i}")
            enter_slot = var_sol.get_start()
            elapsed_minutes = enter_slot * parameters.time_step
            enter_hour = elapsed_minutes // 60
            enter_minute = elapsed_minutes % 60
            enter_time = Time(hours=enter_hour, minutes=enter_minute, seconds=0)

            air_traffic_flows.append(
                AirTrafficFlow(flight=enter_event.flight, sector=enter_event.sector, enter_time=enter_time)
            )

        return AirTrafficFlowSchedulerOutput(input_=input_, is_feasible=True, air_traffic_flows=air_traffic_flows)
