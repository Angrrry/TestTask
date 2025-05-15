from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field

__all__ = ["User"]


class User(BaseModel):
    id_: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    password_hash: str

    def __eq__(self, other: Any):
        return isinstance(other, self.__class__) and self.id_ == other.id_
