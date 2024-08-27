import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ..model.air_traffic_flow_scheduler.output import AirTrafficFlowSchedulerOutput


class Drawer:
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
        # TODO: べた書きのディレクトリをなんとかする
        # TODO: 軸がちゃんと見えない
        plt.savefig("./data/example/output/num_flows_and_upper.png")
