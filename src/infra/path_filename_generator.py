import configparser
from pathlib import Path

from ..utils.config_util import default_section, read_config


class PathFilenameGenerator:
    config_path_and_filename: configparser.SectionProxy

    def __init__(self, config_section: str = default_section):
        self.config_path_and_filename = read_config(section=config_section)

    def generate_path(self, key=str) -> Path:
        return Path(self.config_path_and_filename.get(key))

    def generate_path_data_raw(self) -> Path:
        return self.generate_path("PATH_DATA").joinpath(self.generate_path("PATH_RAW"))

    def generate_path_data_result(self) -> Path:
        return self.generate_path("PATH_DATA").joinpath(self.generate_path("PATH_RESULT"))

    def generate_filename(self, key=str) -> Path:
        return self.config_path_and_filename.get(key)

    def generate_path_local_log(self) -> Path:
        return self.generate_path("PATH_DATA").joinpath(self.generate_path("PATH_LOG"))
