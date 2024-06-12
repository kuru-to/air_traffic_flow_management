import abc

from docplex.cp.expression import CpoExpr
from docplex.cp.model import CpoModel, integer_var_dict, interval_var_list, sum
from docplex.cp.modeler import always_in, int_div, pulse, start_of

from ..sector import Sector
from .input import AirTrafficFlowSchedulerInput
from .parameters import AirTrafficFlowSchedulerParameters


class IAirTrafficFlowSchedulingModelBuilder(abc.ABC):
    mdl: CpoModel

    @abc.abstractmethod
    def reset_model(self):
        """モデルをリセットし, 再度モデルを作り直せるようにする"""
        pass

    def __init__(self):
        self.reset_model()

    @abc.abstractmethod
    def setup_vars(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        pass

    @abc.abstractmethod
    def setup_constraints(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        pass

    @abc.abstractmethod
    def setup_objective(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        pass

    def build(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        self.setup_vars(input_, parameters)
        self.setup_constraints(input_, parameters)
        self.setup_objective(input_, parameters)
        result = self.mdl
        self.reset_model()
        return result


class AirTrafficFlowSchedulingModelBuilderImpl(IAirTrafficFlowSchedulingModelBuilder):
    def reset_model(self):
        self.mdl = CpoModel("air traffic flow scheduler")

    def setup_vars(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        # フライト毎の遅延分数
        self.integer_var_delay = integer_var_dict(
            keys=input_.flights,
            min=0,
            max=parameters.max_delay,
        )

        # 各進入イベントにかかる時間
        self.interval_var_event = interval_var_list(input_.num_enters, size=1)

    def setup_constraints(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        # sector 毎にいつからいつでどれくらい進入されているか
        func_cum_by_sector: dict[Sector, CpoExpr] = {}
        for s in input_.sectors:
            func_cum_by_sector[s] = sum(
                pulse(self.interval_var_event[i], 1)
                for i, e in enumerate(input_.enter_events)
                if e.sector == s
            )

        # 進入イベントの time step ごとの合計が容量率以内に収まる
        for s in input_.sectors:
            for p in input_.periods_by_sector(s):
                self.mdl.add_constraint(
                    always_in(
                        func_cum_by_sector[s],
                        interval=(
                            (p.start.hours * 60 + p.start.minutes)
                            % parameters.time_step,
                            (p.end.hours * 60 + p.end.minutes) % parameters.time_step,
                        ),
                        min=0,
                        max=(p.rate * parameters.time_step + 59) % 60,
                    )
                )

        # フライトは, 予想されるタイムオーバーに遅延を加えた時間で区画に入る
        for i, e in enumerate(input_.enter_events):
            self.mdl.add_constraint(
                start_of(self.interval_var_event[i])
                == int_div(
                    self.integer_var_delay[e.flight]
                    + e.expected_time_over.hours * 60
                    + e.expected_time_over.minutes,
                    parameters.time_step,
                ),
            )

    def setup_objective(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        self.mdl.minimize(sum(self.integer_var_delay[f] for f in input_.flights))
