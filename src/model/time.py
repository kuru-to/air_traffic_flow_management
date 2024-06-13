from __future__ import annotations

import datetime

from pydantic import BaseModel, Field


class Time(BaseModel):
    hours: int = Field(..., ge=0, le=60)
    minutes: int = Field(..., ge=0, le=60)
    seconds: int = Field(..., ge=0, le=60)

    @property
    def all_minutes(self) -> int:
        """全て分換算した際の分数"""
        return self.hours * 60 + self.minutes

    def slot_number(self, time_step: int) -> int:
        """time step で考えたときに何コマ目にあたるのか

        Args:
            time_step (int): 何分間隔でコマを区切るか

        Returns:
            int: 何コマ目か
        """
        return self.all_minutes // time_step

    def __lt__(self, other: Time) -> bool:
        if self.hours != other.hours:
            return self.hours < other.hours

        if self.minutes != other.minutes:
            return self.minutes < other.minutes

        return self.seconds < other.seconds

    def __sub__(self, other: Time) -> int:
        dif_hours = self.hours - other.hours
        dif_minutes = self.minutes - other.minutes
        dif_seconds = self.seconds - other.seconds
        return dif_hours * 60 * 60 + dif_minutes * 60 + dif_seconds

    @classmethod
    def create(cls, time_str: str) -> Time:
        """文字列から変換する.

        Args:
            time_str (str): %H:%M:%S で表記された文字列

        Returns:
            Time: `time_str` を datetime 型に変換したのち, 時刻の情報を抜き出した型
        """
        time_datetime: datetime.time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
        return cls(hours=time_datetime.hour, minutes=time_datetime.minute, seconds=time_datetime.second)
