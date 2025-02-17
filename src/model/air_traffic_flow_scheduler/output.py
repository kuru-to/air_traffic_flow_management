from itertools import product

from pydantic import BaseModel

from ..air_traffic_flow import AirTrafficFlow
from .input import AirTrafficFlowSchedulerInput


class AirTrafficFlowSchedulerOutput(BaseModel):
    input_: AirTrafficFlowSchedulerInput
    is_feasible: bool
    air_traffic_flows: list[AirTrafficFlow]

    @property
    def total_delay(self) -> int | None:
        """total delay の算出. もしも air_traffic_flow に対応する input_ の enter_event がなかった場合, None を返す"""
        # TODO: コメント通りに実装できていない
        result = 0
        for enter_event, air_traffic_flow in product(self.input_.enter_events, self.air_traffic_flows):
            result += air_traffic_flow.delay(enter_event)
        return result
