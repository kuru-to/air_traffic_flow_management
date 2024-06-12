from src.model.air_traffic_flow_scheduler.input import AirTrafficFlowSchedulerInput
from src.model.air_traffic_flow_scheduler.parameters import (
    AirTrafficFlowSchedulerParameters,
)
from src.model.air_traffic_flow_scheduler.scheduling_model_builder import (
    AirTrafficFlowSchedulingModelBuilderImpl,
)
from src.model.enter_event import EnterEvent
from src.model.period import Period
from src.model.sector import Sector


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
            EnterEvent.create(1, sector_name, {"hours": 0, "minutes": 10, "seconds": 0})
        ],
    )
    parameters = AirTrafficFlowSchedulerParameters()

    model_builder = AirTrafficFlowSchedulingModelBuilderImpl()
    model = model_builder.build(input_, parameters)
    solution = model.solve()
    assert solution.is_solution()
    # TODO: テストの結果を図示できるようにする
