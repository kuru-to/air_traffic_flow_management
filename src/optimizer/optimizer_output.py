from abc import ABCMeta, abstractmethod

from ..logger.logger import get_main_logger
from .optimizer_input import OptimizerInput

logger = get_main_logger()


class OptimizedResultInterface(metaclass=ABCMeta):
    """Optimizer が出力する最適解に関するインターフェース
    """
    @abstractmethod
    def display(self, input_: OptimizerInput):
        """最適化による結果を出力する
        """
        pass


class InfeasibleResult(OptimizedResultInterface):
    """問題が実行不可能だった場合に出力される None Class
    """
    def display(self, input_: OptimizerInput):
        """実行不可能であった旨を表示
        """
        logger.warning("Infeasible!")


class OptimizedResult(OptimizedResultInterface):
    """最適化によって出力される結果についてまとめたクラス

    作成する問題によって解となるクラスインスタンスが異なるので, 都度作成すること

    Attributes:
        elapsed_time: 最適化にかかった時間
        sol_objective: 解いた結果の目的関数値
    """
    elapsed_time: float
    sol_objective: float

    def display_basic_information(self):
        """最適解に対する基本的な情報を表示する"""
        logger.info("********")
        logger.info("Result")
        logger.info("********")
        logger.info(f"Objective value = {self.sol_objective}")
        logger.info("********")

    def display_result_detail(self, input_: OptimizerInput):
        """最適解に関する詳細について情報を表示する"""
        pass

    def display(self, input_: OptimizerInput):
        """最適化による結果を出力する

        Args:
            result: 最適解に関する情報. 既に出力されていると考えてよい
        """
        self.display_basic_information()
        self.display_result_detail(input_)
