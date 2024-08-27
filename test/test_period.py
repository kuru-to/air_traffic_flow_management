import pytest

from src.model.period import Period
from src.model.time import Time


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


def test_in_period():
    period = Period.create("test_sector", 0, 10, 0, 0, 20, 0, 1)
    assert not period.is_in_period(Time.create(0, 9, 59))
    assert period.is_in_period(Time.create(0, 10, 0))
    assert period.is_in_period(Time.create(0, 20, 0))
    assert not period.is_in_period(Time.create(0, 20, 1))
