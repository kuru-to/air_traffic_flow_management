from pydantic import BaseModel, Field


class Flight(BaseModel, frozen=True):
    id_: int = Field(..., ge=0)
