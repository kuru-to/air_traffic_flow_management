import pytest

from src.model.period import Period


def test_period_starts_before_end():
    with pytest.raises(ValueError):
        Period.create(
            "test_sector",
            0,
            0,
            10,
            0,
            0,
            0,
            10,
        )
