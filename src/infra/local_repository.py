from pathlib import Path

from ..model.air_traffic_flow import AirTrafficFlow
from ..model.air_traffic_flow_scheduler.parameters import (
    AirTrafficFlowSchedulerParameters,
)
from ..model.enter_event import EnterEvent
from ..model.period import Period
from ..model.repository import IRepository
from ..utils.file_util import read_instances_from_csv, write_instances_to_csv
from .path_filename_generator import PathFilenameGenerator


class LocalRepository(IRepository):
    path_filename_generator: PathFilenameGenerator

    def __init__(self, path_filename_generator: PathFilenameGenerator):
        self.path_filename_generator = path_filename_generator

    def get_path_data_raw(self) -> Path:
        return self.path_filename_generator.generate_path_data_raw()

    def read_periods(self) -> list[Period]:
        filename = self.path_filename_generator.generate_filename("FILENAME_PERIODS")
        results = read_instances_from_csv(
            self.get_path_data_raw(),
            filename,
            Period.create,
            "sector_name,start_hour,start_minute,start_second,end_hour,end_minute,end_second,rate".split(","),
        )
        return results

    def read_enter_events(self) -> list[EnterEvent]:
        filename = self.path_filename_generator.generate_filename("FILENAME_ENTER_EVENTS")
        results = read_instances_from_csv(
            self.get_path_data_raw(),
            filename,
            EnterEvent.create,
            "flight,sector,eto_hour,eto_minute,eto_second".split(","),
        )
        return results

    def read_parameters(self) -> AirTrafficFlowSchedulerParameters:
        """特に現在ファイルに起こしていないのでデフォルト値を出力"""
        return AirTrafficFlowSchedulerParameters()

    def get_path_data_result(self) -> Path:
        return self.path_filename_generator.generate_path_data_result()

    def write_air_traffic_flows(self, air_traffic_flows: list[AirTrafficFlow]):
        filename = self.path_filename_generator.generate_filename("FILENAME_AIR_TRAFFIC_FLOWS")
        write_instances_to_csv(
            self.get_path_data_result(),
            filename,
            [a.model_dump() for a in air_traffic_flows],
            AirTrafficFlow.to_header(),
        )

    def read_air_traffic_flows(self) -> list[AirTrafficFlow]:
        filename = self.path_filename_generator.generate_filename("FILENAME_AIR_TRAFFIC_FLOWS")
        results = read_instances_from_csv(
            self.get_path_data_result(), filename, AirTrafficFlow.create, AirTrafficFlow.to_header()
        )
        return results

    def get_path_local_log(self) -> Path:
        return self.path_filename_generator.generate_path_local_log()
