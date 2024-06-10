# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 10:15:02 2020

最適化問題を設定する際のインターフェース
パッケージどれ使うかの詳細には触れず, どういった形式で実装すべきかを設定
"""
from abc import ABCMeta, abstractmethod

from ..logger.logger import get_main_logger
from .optimizer_parameters import OptimizationParameters, BusinessRuleParameters
from .optimizer_input import OptimizerInput
from .optimizer_output import OptimizedResult

logger = get_main_logger()


class OptimizerInterface(metaclass=ABCMeta):
    """最適化を実行するインターフェース

    実装する際は使用パッケージ, 定式化によってやることが異なるが, 大枠で見れば同じ挙動をする

    Example:
        >>> Optimizer(anOptimizationParameters).run(OptimizationConstants)
            与えられたパラメータと定数により最適化が実行される

    TODO:
        * 初期点を設定できるようにする
    """
    def __init__(
        self,
        parameters: OptimizationParameters,
    ):
        """初期化

        Args:
            _parameters: 開発者が設定する最適化に関わるパラメータ
        """
        self._parameters = parameters

    @abstractmethod
    def validate(
        self,
        input_: OptimizerInput,
        constants: BusinessRuleParameters
    ):
        """最適化を実行する前に入力がおかしいと判断できるものをはじく

        Args:
            input_ (OptimizerInput): 入力
            constants: ユーザーが設定する定数
        """
        pass

    @abstractmethod
    def solve(
        self,
        input_: OptimizerInput,
        constants: BusinessRuleParameters
    ) -> OptimizedResult:
        """求解してその結果を保持する

        モデルによって行うことがことなるので `abstractmethod`. 必ず実装する
        """
        pass

    def run(
        self,
        input_: OptimizerInput,
        constants: BusinessRuleParameters
    ) -> OptimizedResult:
        """全てを実行して最適化を行う関数
        Infeasible になる可能性もありうる
        """
        logger.info("Start validate input data.")
        self.validate(input_, constants)
        logger.info("End validate input data.")

        logger.info("Start solving problem.")
        output = self.solve(input_, constants)
        logger.info("End solving problem.")

        output.display(input_)
        return output
