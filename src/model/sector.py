from pydantic import BaseModel


class Sector(BaseModel, frozen=True):
    name: str
