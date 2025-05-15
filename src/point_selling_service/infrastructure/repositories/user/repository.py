import logging

from point_selling_service.domain.model import IUserRepository, User
from sqlalchemy.orm import Session
from sqlalchemy import desc
from .mappers import TransactionMapper, UserMapper, GetUserResponse
from .query_factory import UserQueryFactory
from datetime import datetime

__all__ = ["UserRepository"]

from ..tables import TransactionTable, UserTable


class UserRepository(IUserRepository):
    def __init__(self, database_engine):
        self._database_engine = database_engine
        self._query_factory = UserQueryFactory()
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user(self, id_: str) -> User | None:
        with Session(self._database_engine) as session:
            # TODO: optimize it to run with one query
            user_table_output = session.execute(
                self._query_factory.select_user_table(id_).first()
            ).scalar()
            if not user_table_output:
                return None
            last_transaction_data = session.execute(
                self._query_factory.select_last_transaction_id_of_user(id_).first()
            ).scalar()
            money_total = session.execute(
                self._query_factory.select_total_money_amount(id_).first()
            ).scalar()
            points_total = session.execute(
                self._query_factory.select_total_points_amount(id_).first()
            ).scalar()
        user_data = GetUserResponse(
            id=user_table_output.id,
            name=user_table_output.name,
            last_transaction_id=last_transaction_data,
            money_total=money_total,
            points_total=points_total,
        )
        return UserMapper.from_response(user_data)

    def save_user(self, user: User) -> None:
        with Session(self._database_engine) as session:
            session.add_all([*map(TransactionMapper.to_table_model, user.transactions)])
            session.commit()

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
