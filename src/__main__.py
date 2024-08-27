"""Main module for running this package."""

import argparse

from .app.main_process import run_main_process
from .infra.cplex.scheduler import AirTrafficFlowScheduler
from .infra.cplex.scheduling_model_builder import (
    AirTrafficFlowSchedulingModelBuilderImpl,
)
from .infra.drawer import Drawer
from .infra.local_repository import LocalRepository
from .infra.path_filename_generator import PathFilenameGenerator
from .logger.logger import setup_logger
from .utils.config_util import default_section


def main(config_section: str):
    path_filename_generator = PathFilenameGenerator(config_section)
    repository = LocalRepository(path_filename_generator)
    scheduler = AirTrafficFlowScheduler(AirTrafficFlowSchedulingModelBuilderImpl(), path_filename_generator)
    drawer = Drawer(path_filename_generator)

    setup_logger("main", path_log=path_filename_generator.generate_path_local_log())

    run_main_process(scheduler, repository, drawer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-cs", "--config_section", help="config ファイルで使用するセクション名", default=default_section
    )
    args = parser.parse_args()

    main(args.config_section)
