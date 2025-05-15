from typing import Protocol
from .user import User

__all__ = ["IUserRepository"]


class IUserRepository(Protocol):
    def get_user(self, id_: str) -> User | None: ...
    def save_user(self, user: User) -> None: ...
    def get_users(self, **id_: str) -> list[User]: ...
    def get_user_with_filtered_transactions(
        self,
        order_by: str | None = None,
        type_: str = None,
        ascending: bool = True,
        receiver: str | None = None,
        before: datetime | None = None,
        after: datetime | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[User]: ...
