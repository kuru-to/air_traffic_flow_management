from pydantic import BaseModel, Field


class Flight(BaseModel):
    id_: int = Field(..., ge=0)
