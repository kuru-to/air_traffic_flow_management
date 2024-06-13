from src.infra.local_repository import LocalRepository
from src.utils.config_util import test_section

test_repository = LocalRepository(test_section)


def test_read_sectors():
    sectors = test_repository.read_sectors()

    assert len(sectors) == 2


def test_read_periods():
    sectors = test_repository.read_periods()

    assert len(sectors) == 2
