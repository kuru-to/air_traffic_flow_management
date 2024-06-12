import pytest
from pydantic import ValidationError

from src.model.time import Time


def test_raise_error_with_less_than_zero():
    with pytest.raises(ValidationError):
        Time(hours=0, minutes=0, seconds=-1)


def test_calculate_num_of_slot_by_time_step():
    """time step をもとにその時刻が何コマ目かを計算するテスト"""
    assert Time(hours=2, minutes=35, seconds=40).num_slot(10) == ((2 * 60) + 35) % 10


def test_subtraction():
    """引き算ができるか"""
    assert (
        Time(hours=1, minutes=1, seconds=0) - Time(hours=0, minutes=0, seconds=0)
        == 60 * 60 * 1 + 60 * 1
    )
