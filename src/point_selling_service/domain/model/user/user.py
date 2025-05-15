from typing import Any
from uuid import uuid4
from .business_exceptions import NotEnoughMoneyException
from .transaction import Transaction, SYSTEM_IDENTITY_ID, TransactionType
from pydantic import BaseModel, Field

__all__ = ["User"]


class User(BaseModel):
    id_: str = Field(default_factory=lambda: uuid4().hex)
    name: str
    points_balance: float
    money_balance: float
    transactions: list[Transaction] = Field(default_factory=list)
    last_transaction_id: str | None

    def __eq__(self, other: Any):
        return isinstance(other, self.__class__) and self.id_ == other.id_

    def buy_points(self, point_price: float, points_amount: float) -> None:
        money_to_spend = point_price * points_amount
        self._check_is_enough_money(money_to_spend)
        self._apply_transaction(
            from_=self.id_,
            to_=SYSTEM_IDENTITY_ID,
            money_spent=money_to_spend,
            points_spent=points_amount,
            transaction_type=TransactionType.POINTS_ACQUIRING,
        )

    def top_up_balance(self, money_amount: float) -> None:
        self._apply_transaction(
            from_=SYSTEM_IDENTITY_ID,
            to_=self.id_,
            money_spent=-money_amount,
            points_spent=0.0,
            transaction_type=TransactionType.TOP_UP,
        )

    def transfer_to(self, money_amount: float, receiver: "User") -> None:
        self._check_is_enough_money(money_amount)
        self._apply_transaction(
            from_=self.id_,
            to_=receiver.id_,
            money_spent=money_amount,
            points_spent=0.0,
            transaction_type=TransactionType.TRANSFER,
        )

    def service_fee(self, fee_amount: float):
        self._apply_transaction(
            from_=self.id_,
            to_=SYSTEM_IDENTITY_ID,
            money_spent=fee_amount,
            points_spent=0.0,
            transaction_type=TransactionType.SERVICE_FEE,
        )

    def _apply_transaction(
        self,
        *,
        from_: str,
        to_: str,
        money_spent: float,
        points_spent: float,
        transaction_type: TransactionType,
    ) -> None:
        new_transaction = self._create_transaction(
            from_=from_,
            to_=to_,
            money_spent=money_spent,
            points_spent=points_spent,
            transaction_type=transaction_type,
        )
        self.money_balance -= money_spent
        self.points_balance -= points_spent
        self.transactions.append(new_transaction)

    def _create_transaction(
        self,
        *,
        from_: str,
        to_: str,
        money_spent: float,
        points_spent: float,
        transaction_type: TransactionType,
    ) -> Transaction:
        return Transaction(
            from_=from_,
            to=to_,
            money_delta=money_spent,
            points_delta=points_spent,
            transaction_type=transaction_type,
        )

    def _check_is_enough_money(self, amount_required: float) -> None:
        if amount_required > self.money_balance:
            raise NotEnoughMoneyException(
                f"Not enough money to buy {amount_required} points"
            )
