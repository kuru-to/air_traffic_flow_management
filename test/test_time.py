import pytest
from pydantic import ValidationError

from src.model.time import Time


def test_raise_error_with_less_than_zero():
    with pytest.raises(ValidationError):
        Time(hours=0, minutes=0, seconds=-1)


def test_calculate_slot_number_by_time_step():
    """time step をもとにその時刻が何コマ目かを計算するテスト"""
    assert Time(hours=2, minutes=35, seconds=40).slot_number(10) == 2 * 6 + 3


def test_subtraction():
    """引き算ができるか"""
    assert Time(hours=1, minutes=1, seconds=0) - Time(hours=0, minutes=0, seconds=0) == 60 * 60 * 1 + 60 * 1


def test_create():
    """%H:%M:%S の文字列が与えられたときに正しく変換できるか"""
    hours = "00"
    minutes = "10"
    seconds = "20"
    test_obj = Time.create(f"{hours}:{minutes}:{seconds}")

    assert test_obj.hours == int(hours)
    assert test_obj.minutes == int(minutes)
    assert test_obj.seconds == int(seconds)
