import os

from src.infra.local_repository import LocalRepository
from src.infra.path_filename_generator import PathFilenameGenerator
from src.model.air_traffic_flow import AirTrafficFlow
from src.utils.config_util import read_config, test_section
from src.utils.file_util import remove_files_and_dirs

test_repository = LocalRepository(PathFilenameGenerator(test_section))


def test_read_periods():
    sectors = test_repository.read_periods()

    assert len(sectors) == 2


def test_read_enter_events():
    enter_events = test_repository.read_enter_events()

    assert len(enter_events) == 2


def test_write_air_traffic_flows():
    # setup: テスト対象のファイルを削除
    test_config = read_config(section=test_section)
    sol_path = (
        test_config.get("PATH_DATA") + test_config.get("PATH_RESULT") + test_config.get("FILENAME_AIR_TRAFFIC_FLOWS")
    )
    remove_files_and_dirs([sol_path])

    sol_objs = [AirTrafficFlow.create(1, "test_sector", 0, 0, 0)]
    test_repository.write_air_traffic_flows(sol_objs)

    assert os.path.exists(sol_path)

    test_objs = test_repository.read_air_traffic_flows()
    assert len(sol_objs) == len(test_objs)
    for test_obj, sol_obj in zip(test_objs, sol_objs):
        assert test_obj == sol_obj
