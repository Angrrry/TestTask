from point_selling_service.domain.model import IUserRepository, User
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from .mapper import UserMapper
from ..tables import UserTable

__all__ = ["UserRepository"]

class UserRepository(IUserRepository):
    def __init__(self, connection_string: str):
        self._engine= create_engine(connection_string)

    def get_user(self, id_: str) -> User | None:
        with Session(self._engine) as session:
            user_table = session.execute(select(UserTable).where(UserTable.id == id_)).scalar_one_or_none()
        return user_table and UserMapper.from_table(user_table)

    def save_user(self, user: User) -> None:
        with Session(self._engine) as session:
            session.merge(user)
            session.commit()
