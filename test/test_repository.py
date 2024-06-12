from src.infra.local_repository import LocalRepository
from src.utils.config_util import test_section


def test_read_sectors():
    repository = LocalRepository(test_section)
    sectors = repository.read_sectors()

    assert len(sectors) == 2
