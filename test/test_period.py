import pytest

from src.model.period import Period


def test_period_starts_before_end():
    with pytest.raises(ValueError):
        Period.create(
            "test_sector",
            "00:00:10",
            "00:00:00",
            10,
        )
