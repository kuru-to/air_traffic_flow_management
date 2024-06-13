import pytest

from src.model.air_traffic_flow_scheduler.input import AirTrafficFlowSchedulerInput
from src.model.air_traffic_flow_scheduler.parameters import AirTrafficFlowSchedulerParameters
from src.model.air_traffic_flow_scheduler.scheduler import AirTrafficFlowScheduler
from src.model.air_traffic_flow_scheduler.scheduling_model_builder import AirTrafficFlowSchedulingModelBuilderImpl
from src.model.enter_event import EnterEvent
from src.model.period import Period
from src.model.sector import Sector

sector_name = "test_sector"
input_ = AirTrafficFlowSchedulerInput(
    sectors=[Sector(name=sector_name)],
    periods=[
        Period.create(
            sector_name,
            "00:00:00",
            "00:30:00",
            30,
        )
    ],
    enter_events=[
        EnterEvent.create(1, sector_name, "00:10:00"),
        EnterEvent.create(2, sector_name, "00:20:00"),
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
    model_output = AirTrafficFlowScheduler().run(input_, parameters, model_builder)
    assert model_output.total_delay == 0


@pytest.mark.local_cplex
def _test_output_infeasible_case():
    input_ = AirTrafficFlowSchedulerInput(
        sectors=[Sector(name=sector_name)],
        periods=[
            Period.create(
                sector_name,
                "00:00:00",
                "00:10:00",
                1,
            )
        ],
        enter_events=[
            EnterEvent.create(1, sector_name, "00:10:00"),
            EnterEvent.create(2, sector_name, "00:10:00"),
        ],
    )
    model_output = AirTrafficFlowScheduler().run(input_, parameters, model_builder)
    assert not model_output.is_feasible
