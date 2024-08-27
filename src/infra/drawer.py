import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ..model.air_traffic_flow_scheduler.output import AirTrafficFlowSchedulerOutput
from .path_filename_generator import PathFilenameGenerator


class Drawer:
    path_filename_generator: PathFilenameGenerator

    def __init__(self, path_filename_generator: PathFilenameGenerator):
        self.path_filename_generator = path_filename_generator

    def draw_num_flights_by_period(self, model_output: AirTrafficFlowSchedulerOutput):
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
