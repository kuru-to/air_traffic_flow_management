import configparser
from pathlib import Path

from ..model.air_traffic_flow import AirTrafficFlow
from ..model.enter_event import EnterEvent
from ..model.period import Period
from ..model.repository import IRepository
from ..model.sector import Sector
from ..utils.config_util import default_section, read_config
from ..utils.file_util import read_instances_from_csv, write_instances_to_csv


class LocalRepository(IRepository):
    config_path_and_filename: configparser.SectionProxy

    def __init__(self, config_section: str = default_section):
        self.config_path_and_filename = read_config(section=config_section)

    def get_path(self, key=str) -> Path:
        return Path(self.config_path_and_filename.get(key))

    def get_path_data_raw(self) -> Path:
        return self.get_path("PATH_DATA").joinpath(self.get_path("PATH_RAW"))

    def read_sectors(self) -> list[Sector]:
        filename = self.config_path_and_filename.get("FILENAME_SECTORS")
        results = read_instances_from_csv(self.get_path_data_raw(), filename, Sector, ["name"])
        return results

    def read_periods(self) -> list[Period]:
        filename = self.config_path_and_filename.get("FILENAME_PERIODS")
        results = read_instances_from_csv(
            self.get_path_data_raw(), filename, Period.create, "sector_name,start_time,end_time".split(",")
        )
        return results

    def read_enter_events(self) -> list[EnterEvent]:
        filename = self.config_path_and_filename.get("FILENAME_ENTER_EVENTS")
        results = read_instances_from_csv(
            self.get_path_data_raw(), filename, EnterEvent.create, "flight,sector,eto".split(",")
        )
        return results

    def get_path_data_result(self) -> Path:
        return self.get_path("PATH_DATA").joinpath(self.get_path("PATH_RESULT"))

    def write_air_traffic_flows(self, air_traffic_flows: list[AirTrafficFlow]):
        filename = self.config_path_and_filename.get("FILENAME_AIR_TRAFFIC_FLOWS")
        write_instances_to_csv(
            self.get_path_data_result(),
            filename,
            [a.model_dump() for a in air_traffic_flows],
            AirTrafficFlow.model_fields.keys(),
        )

    def read_air_traffic_flows(self) -> list[AirTrafficFlow]:
        filename = self.config_path_and_filename.get("FILENAME_AIR_TRAFFIC_FLOWS")
        results = read_instances_from_csv(
            self.get_path_data_result(), filename, AirTrafficFlow.create, "flight,sector,enter_time".split(",")
        )
        return results
