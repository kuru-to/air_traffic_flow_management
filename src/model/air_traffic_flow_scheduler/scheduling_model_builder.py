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

    def setup_vars(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        for func_name in dir(self):
            if func_name.startswith("_set_dvars_"):
                eval(
                    f"self.{func_name}(input_, parameters)",
                    {},
                    {"self": self, "input_": input_, "parameters": parameters},
                )

    def setup_constraints(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        for func_name in dir(self):
            if func_name.startswith("_add_constraints_"):
                eval(
                    f"self.{func_name}(input_, parameters)",
                    {},
                    {"self": self, "input_": input_, "parameters": parameters},
                )

    def setup_objective(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        obj = 0
        for func_name in dir(self):
            if func_name.startswith("_get_objective_function_"):
                obj += eval(
                    f"self.{func_name}(input_, parameters)",
                    {},
                    {"self": self, "input_": input_, "parameters": parameters},
                )

        self.mdl.minimize(obj)

    def build(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        self.reset_model()
        self.setup_vars(input_, parameters)
        self.setup_constraints(input_, parameters)
        self.setup_objective(input_, parameters)
        return self.mdl


class AirTrafficFlowSchedulingModelBuilderImpl(IAirTrafficFlowSchedulingModelBuilder):
    def reset_model(self):
        # TODO: log の吐き出し先指定
        self.mdl = CpoModel("air traffic flow scheduler")

    def _set_dvars_all(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        # フライト毎の遅延分数
        self.integer_var_delay = integer_var_dict(keys=input_.flights, min=0, max=parameters.max_delay, name="delay")

        # 各進入イベントにかかる時間
        self.interval_var_event = interval_var_list(
            input_.num_enters, size=parameters.interval_size, name="interval_event"
        )

    def _add_constraints_all(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ):
        # sector 毎にいつからいつでどれくらい進入されているか
        func_cum_by_sector: dict[Sector, CpoExpr] = {}
        for s in input_.sectors:
            func_cum_by_sector[s] = sum(
                pulse(self.interval_var_event[i], 1) for i, e in enumerate(input_.enter_events) if e.sector == s
            )

        # 進入イベントの time step ごとの合計が容量率以内に収まる
        for s in input_.sectors:
            for p in input_.periods_by_sector(s):
                self.mdl.add_constraint(
                    always_in(
                        func_cum_by_sector[s],
                        interval=(
                            p.start.slot_number(parameters.time_step),
                            p.end.slot_number(parameters.time_step),
                        ),
                        min=0,
                        max=(p.rate * parameters.time_step + 59) // 60,
                    )
                )

        # フライトは, 予想されるタイムオーバーに遅延を加えた時間で区画に入る
        for i, e in enumerate(input_.enter_events):
            self.mdl.add_constraint(
                start_of(self.interval_var_event[i])
                == int_div(
                    self.integer_var_delay[e.flight] + e.expected_time_over.all_minutes,
                    parameters.time_step,
                ),
            )

    def _get_objective_function_delay(
        self,
        input_: AirTrafficFlowSchedulerInput,
        parameters: AirTrafficFlowSchedulerParameters,
    ) -> CpoExpr:
        return sum(self.integer_var_delay[f] for f in input_.flights)
