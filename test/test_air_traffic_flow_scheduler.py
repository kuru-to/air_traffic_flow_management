import pytest

from src.infra.cplex.scheduler import AirTrafficFlowScheduler
from src.infra.cplex.scheduling_model_builder import (
    AirTrafficFlowSchedulingModelBuilderImpl,
)
from src.infra.path_filename_generator import PathFilenameGenerator
from src.model.air_traffic_flow_scheduler.input import AirTrafficFlowSchedulerInput
from src.model.air_traffic_flow_scheduler.parameters import (
    AirTrafficFlowSchedulerParameters,
)
from src.model.enter_event import EnterEvent
from src.model.period import Period
from src.model.sector import Sector
from src.utils.config_util import test_section

sector_name = "test_sector"
input_ = AirTrafficFlowSchedulerInput(
    sectors=[Sector(name=sector_name)],
    periods=[
        Period.create(
            sector_name,
            0,
            0,
            0,
            0,
            30,
            0,
            30,
        )
    ],
    enter_events=[
        EnterEvent.create(1, sector_name, 0, 10, 0),
        EnterEvent.create(2, sector_name, 0, 20, 0),
    ],
)
parameters = AirTrafficFlowSchedulerParameters()
model_builder = AirTrafficFlowSchedulingModelBuilderImpl()


@pytest.mark.local_cplex
def test_optimize():
    model = model_builder.build(input_, parameters)
    solution = model.solve()

    assert solution.is_solution()
    for i, enter_event in enumerate(input_.enter_events):
        var_sol = solution.get_var_solution(f"interval_event_{i}")
        assert var_sol.get_start() == enter_event.expected_time_over.slot_number(parameters.time_step)
        assert var_sol.get_end() == enter_event.expected_time_over.slot_number(parameters.time_step) + 1
    for i, _ in enumerate(input_.flights):
        delay_sol = solution.get_var_solution(f"delay_{i}")
        assert delay_sol.get_value() == 0


@pytest.mark.local_cplex
def test_scheduler_run():
    model_output = AirTrafficFlowScheduler(model_builder, PathFilenameGenerator(test_section)).run(input_, parameters)
    assert model_output.total_delay == 0
