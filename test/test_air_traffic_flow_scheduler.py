import pytest

from src.model.air_traffic_flow_scheduler.input import AirTrafficFlowSchedulerInput
from src.model.air_traffic_flow_scheduler.parameters import AirTrafficFlowSchedulerParameters
from src.model.air_traffic_flow_scheduler.scheduling_model_builder import AirTrafficFlowSchedulingModelBuilderImpl
from src.model.enter_event import EnterEvent
from src.model.period import Period
from src.model.sector import Sector
from src.utils.config_util import read_config, test_section

config_path_name = read_config(section=test_section)


@pytest.mark.local_cplex
def test_optimize():
    sector_name = "test_sector"
    input_ = AirTrafficFlowSchedulerInput(
        sectors=[Sector(name=sector_name)],
        periods=[
            Period.create(
                sector_name,
                {"hours": 0, "minutes": 0, "seconds": 0},
                {"hours": 0, "minutes": 30, "seconds": 0},
                30,
            )
        ],
        enter_events=[
            EnterEvent.create(1, sector_name, {"hours": 0, "minutes": 10, "seconds": 0}),
            EnterEvent.create(2, sector_name, {"hours": 0, "minutes": 20, "seconds": 0}),
        ],
    )
    parameters = AirTrafficFlowSchedulerParameters()

    model_builder = AirTrafficFlowSchedulingModelBuilderImpl()
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
