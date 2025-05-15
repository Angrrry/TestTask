from typing import Protocol
from .user import User
from datetime import datetime
__all__ = ["IUserRepository"]


class IUserRepository(Protocol):
    def get_user(self, id_: str) -> User | None: ...
    def save_user(self, user: User) -> None: ...