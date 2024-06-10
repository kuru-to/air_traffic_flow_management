"""ソルバーを用いて最適化する際のインターフェース
"""
from abc import ABCMeta, abstractmethod
import time

from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution

from ..logger.logger import get_main_logger
from .optimizer_parameters import BusinessRuleParameters, OptimizationParameters
from .optimizer_input import OptimizerInput
from .optimizer import OptimizerInterface
from .optimizer_output import OptimizedResult, InfeasibleResult

logger = get_main_logger()


class CplexOptimizer(OptimizerInterface, metaclass=ABCMeta):
    """ソルバーを用いて最適化を実行するインターフェース

    主に定式化等を扱う

    Example:
        >>> Optimizer(anOptimizationParameters).run(OptimizerInput)
            与えられたパラメータと定数により最適化が実行される
    """
    _model: Model

    def __init__(self, parameters: OptimizationParameters):
        super().__init__(parameters)

        # Setup optimization model
        self._model = Model(name=parameters.MODEL_NAME)
        self._model.set_time_limit(parameters.MAX_SECONDS)

    @abstractmethod
    def build(self, _input: OptimizerInput, constants: BusinessRuleParameters):
        """ソルバーが解くモデルの作成

        変数, 目的関数, 制約を設定する
        """
        pass

    @abstractmethod
    def make_result(self, solution: SolveSolution, elapsed_time: float) -> OptimizedResult:
        """最適化の結果から出力を出す
        """
        pass

    def solve(
        self,
        input_: OptimizerInput,
        constants: BusinessRuleParameters
    ) -> OptimizedResult:
        """求解してその結果を保持する

        測定する計算時間は, 定数の設定開始~求解完了まで
        """
        start_time = time.time()

        logger.info("Start building problem.")
        self.build(input_, constants)
        logger.info("End building problem.")

        with open(self._parameters.CPLEX_LOG_FILE, mode="a+") as f:
            solution = self._model.solve(log_output=f)

        if self._model.solve_details.status == "infeasible":
            return InfeasibleResult()

        result = self.make_result(solution, time.time() - start_time)
        return result
