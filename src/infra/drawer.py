import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ..logger.logger import get_main_logger
from ..model.air_traffic_flow_scheduler.output import AirTrafficFlowSchedulerOutput
from .path_filename_generator import PathFilenameGenerator

logger = get_main_logger()


def deco_logging(doing: str):
    """実行開始・終了を logging するためのデコレータ"""

    def _deco_logging(func):
        def wrapper(*args, **kwargs):
            logger.info(f"Start {doing}...")
            func(*args, **kwargs)
            logger.info(f"Finish {doing}.")

        return wrapper

    return _deco_logging


class Drawer:
    path_filename_generator: PathFilenameGenerator

    def __init__(self, path_filename_generator: PathFilenameGenerator):
        self.path_filename_generator = path_filename_generator

    @deco_logging("drawing num flights by period")
    def draw_num_flights_by_period(self, model_output: AirTrafficFlowSchedulerOutput):
        """各 period ごとの flight 数と, rate から算出される period の上限フライト数を棒グラフ描画"""
        periods = model_output.input_.periods

        num_flows_by_period = {
            f"{p.sector}_{p.start}-{p.end}": len(
                [a for a in model_output.air_traffic_flows if p.sector == a.sector and p.is_in_period(a.enter_time)]
            )
            for p in periods
        }
        df_num_flows = pd.DataFrame.from_dict(num_flows_by_period, orient="index", columns=["num"]).reset_index()
        df_num_flows["type"] = "num_enter"

        upper_by_period = {f"{p.sector}_{p.start}-{p.end}": p.upper_flights_by_hour for p in periods}
        df_upper = pd.DataFrame.from_dict(upper_by_period, orient="index", columns=["num"]).reset_index()
        df_upper["type"] = "upper"

        df = pd.concat([df_num_flows, df_upper])
        sns.barplot(data=df, x="num", y="index", hue="type")
        # TODO: 軸がちゃんと見えない
        path_result = self.path_filename_generator.generate_path_data_result()
        plt.savefig(
            path_result.joinpath(self.path_filename_generator.generate_filename("FILENAME_PNG_NUM_FLOWS_AND_UPPER"))
        )

    @deco_logging("drawing delay histogram")
    def draw_delay_histogram(self, model_output: AirTrafficFlowSchedulerOutput):
        """各 enter_event の遅延分数をヒストグラムで描画"""
        delays = [
            sum(a.delay(e) // 60 for a in model_output.air_traffic_flows) for e in model_output.input_.enter_events
        ]

        fig, ax = plt.subplots(1, 1, dpi=300)
        ax = sns.histplot(
            data=delays,
        )
        ax.set_xlabel("delay minutes")
        ax.set_ylabel("count")

        path_result = self.path_filename_generator.generate_path_data_result()
        fig.savefig(
            path_result.joinpath(self.path_filename_generator.generate_filename("FILENAME_PNG_DELAY_HISTOGRAM"))
        )

    def run(self, model_output: AirTrafficFlowSchedulerOutput):
        self.draw_num_flights_by_period(model_output)
        self.draw_delay_histogram(model_output)
