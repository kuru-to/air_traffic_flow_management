from __future__ import annotations

from pydantic import BaseModel, Field


class Time(BaseModel):
    hours: int = Field(..., ge=0, le=60)
    minutes: int = Field(..., ge=0, le=60)
    seconds: int = Field(..., ge=0, le=60)

    def num_slot(self, time_step: int) -> int:
        """time step で考えたときに何コマ目にあたるのか

        Args:
            time_step (int): 何分間隔でコマを区切るか

        Returns:
            int: 何コマ目か
        """
        return (self.hours * 60 + self.minutes) % time_step

    def __lt__(self, other: Time) -> bool:
        if self.hours != other.hours:
            return self.hours < other.hours

        if self.minutes != other.minutes:
            return self.minutes < other.minutes

        return self.seconds < other.seconds
