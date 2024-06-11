import pytest

from src.model.period import Period


def test_period_starts_before_end():
    with pytest.raises(ValueError):
        Period.create(
            "test_sector",
            {"hours": 0, "minutes": 0, "seconds": 10},
            {"hours": 0, "minutes": 0, "seconds": 0},
            10,
        )
