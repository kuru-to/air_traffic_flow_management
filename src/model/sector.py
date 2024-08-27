from pydantic import BaseModel


class Sector(BaseModel, frozen=True):
    name: str

    def __str__(self) -> str:
        return self.name
