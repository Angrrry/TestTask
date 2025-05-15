from dataclasses import dataclass
from point_selling_service.domain.model import Transaction, User
from ..tables import TransactionTable

__all__ = ["GetUserResponse", "UserMapper"]


@dataclass
class GetUserResponse:
    id: str
    name: str
    last_transaction_id: str | None
    money_total: float
    points_total: float


class UserMapper:
    @classmethod
    def from_response(self, user_data: GetUserResponse) -> User:
        return User(
            id_=user_data.id,
            name=user_data.name,
            points_balance=user_data.points_total,
            money_balance=user_data.money_total,
            last_transaction_id=user_data.last_transaction_id,
        )


class TransactionMapper:
    @classmethod
    def to_table_model(cls, transaction: Transaction) -> TransactionTable:
        return TransactionTable(
            id=transaction.id_,
            type=transaction.transaction_type.value,
            previous_transaction_id=transaction.previous_transaction_id,
            points_spent=transaction.points_delta,
            money_spent=transaction.money_delta,
            initiator=transaction.from_,
            recipient=transaction.to,
        )
