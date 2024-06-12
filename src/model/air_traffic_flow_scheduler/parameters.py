import math

from pydantic import BaseModel, field_validator


class AirTrafficFlowSchedulerParameters(BaseModel):
    max_delay: int = 120
    time_step: int = 10
    interval_size: int = 1
    cplex_faillimit: int = 20000

    @field_validator("time_step")
    def validate_common_divisor_of_60(cls, v: int) -> int:
        """time_step は1時間で区切りをつけられるよう, 60の公約数であること"""
        if math.gcd(v, 60) != v:
            raise ValueError(f"time_step({v})は60の公約数である必要があります.")
        return v
