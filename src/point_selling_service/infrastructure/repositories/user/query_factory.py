from sqlalchemy import select, Select, or_, func, insert

from point_selling_service.domain.model import Transaction
from ..tables import UserTable, TransactionTable
from .mappers import TransactionMapper

__all__ = ["UserQueryFactory"]


class UserQueryFactory:
    def select_user_table(self, user_id: str):
        return select(UserTable).where(UserTable.id == user_id)

    def select_last_transaction_id_of_user(self, user_id: str):
        return (
            select(TransactionTable.id)
            .where(
                or_(
                    TransactionTable.initiator == user_id,
                    TransactionTable.recipient == user_id,
                )
            )
            .order_by(TransactionTable.timestamp.desc())
            .limit(1)
        )

    def select_total_money_amount(self, user_id: str):
        money_obtained = func.coalesce(
            func.sum(TransactionTable.money_spent), 0.0
        ).where(TransactionTable.recipient == user_id)

        money_spent = func.coalesce(func.sum(TransactionTable.money_spent), 0.0).where(
            TransactionTable.initiator == user_id
        )
        return select(money_obtained - money_spent).label("money_amount")

    def select_total_points_amount(self, user_id: str):
        points_obtained = func.coalesce(
            func.sum(TransactionTable.points_spent), 0.0
        ).where(TransactionTable.recipient == user_id)
        points_spent = func.coalesce(
            func.sum(TransactionTable.points_spent), 0.0
        ).where(TransactionTable.initiator == user_id)
        return select(points_obtained - points_spent).label("points_amount")
