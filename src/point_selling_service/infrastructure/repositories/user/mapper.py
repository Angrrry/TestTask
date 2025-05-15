from point_selling_service.domain.model import User

__all__ = ["UserMapper"]

from point_selling_service.infrastructure.repositories.tables import UserTable


class UserMapper:
    @classmethod
    def from_domain(cls, user: User) -> UserTable:
        return UserTable(
                id=user.id_,
            name=user.name,
            password_hash=user.password_hash
                )
    @classmethod
    def from_table(cls, user: UserTable) -> User:
        return User(
                id_=user.id,
                name=user.name,
                password_hash=user.password_hash,
                )