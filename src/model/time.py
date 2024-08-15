from __future__ import annotations

from pydantic import BaseModel, Field


class Time(BaseModel, frozen=True):
    hours: int = Field(..., ge=0, le=23)
    minutes: int = Field(..., ge=0, le=59)
    seconds: int = Field(..., ge=0, le=59)

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
        """引き算し, 秒数で出力"""
        dif_hours = self.hours - other.hours
        dif_minutes = self.minutes - other.minutes
        dif_seconds = self.seconds - other.seconds
        return dif_hours * 60 * 60 + dif_minutes * 60 + dif_seconds

    @classmethod
    def create(cls, hour: int, minute: int, second: int) -> Time:
        """3つの int から変換する."""
        return cls(hours=hour, minutes=minute, seconds=second)

    def __str__(self) -> str:
        """%H:%M:%S の形式で文字列出力"""
        return ":".join([str(self.hours).zfill(2), str(self.minutes).zfill(2), str(self.seconds).zfill(2)])
