import contextlib
from datetime import datetime

from docplex.cp.config import context
from docplex.cp.solution import CpoModelSolution

from ...model.air_traffic_flow import AirTrafficFlow
from ...model.air_traffic_flow_scheduler.input import AirTrafficFlowSchedulerInput
from ...model.air_traffic_flow_scheduler.output import AirTrafficFlowSchedulerOutput
from ...model.air_traffic_flow_scheduler.parameters import (
    AirTrafficFlowSchedulerParameters,
)
from ...model.air_traffic_flow_scheduler.scheduler import IAirTrafficFlowScheduler
from ...model.time import Time
from ..path_filename_generator import PathFilenameGenerator
from .scheduling_model_builder import IAirTrafficFlowSchedulingModelBuilder


class AirTrafficFlowScheduler(IAirTrafficFlowScheduler):
    """Air traffic flow についてスケジューリングを行う"""

    model_builder: IAirTrafficFlowSchedulingModelBuilder
    path_filename_generator: PathFilenameGenerator

    def __init__(
        self, model_builder: IAirTrafficFlowSchedulingModelBuilder, path_filename_generator: PathFilenameGenerator
    ):
        self.model_builder = model_builder
        self.path_filename_generator = path_filename_generator

    @contextlib.contextmanager
    def open_cplex_logger(self):
        prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
        cplex_log_filename: str = f"{prefix}_cplex.log"
        log_path = self.path_filename_generator.generate_path_local_log().joinpath(cplex_log_filename)

        fp = open(log_path, "w")
        try:
            yield fp
        finally:
            fp.close()

    def run(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ) -> AirTrafficFlowSchedulerOutput:
        model = self.model_builder.build(input_, parameters)
        with self.open_cplex_logger() as f:
            context.log_output = f
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
