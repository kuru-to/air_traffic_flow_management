from ..infra.drawer import Drawer
from ..logger.logger import get_main_logger
from ..model.air_traffic_flow_scheduler.input import AirTrafficFlowSchedulerInput
from ..model.air_traffic_flow_scheduler.scheduler import IAirTrafficFlowScheduler
from ..model.repository import IRepository


def run_main_process(scheduler: IAirTrafficFlowScheduler, repository: IRepository, drawer: Drawer):
    """ファイルを読み込み, scheduler に結果を出力させ, ファイルへ出力する"""
    logger = get_main_logger()

    logger.info("Start reading files...")
    periods = repository.read_periods()
    enter_events = repository.read_enter_events()
    parameters = repository.read_parameters()
    logger.info("Done reading files.")

    sectors = list(set([p.sector for p in periods]))

    logger.info("Start scheduling...")
    input_ = AirTrafficFlowSchedulerInput(sectors=sectors, periods=periods, enter_events=enter_events)
    output = scheduler.run(input_, parameters)
    logger.info("End scheduling.")

    logger.info("Start writing results...")
    repository.write_air_traffic_flows(output.air_traffic_flows)
    drawer.run(output.air_traffic_flows, input_.periods, input_.enter_events)
    logger.info("End writing results.")
