from pydantic import BaseModel, Field
from uuid import uuid4
from .transaction import Transaction, TransactionType
from ..business_exceptions import UserWalletDataIsOutdated, NotEnoughMoneyException

__all__ = ["Wallet"]

class Wallet(BaseModel):
    id_: str = Field(default_factory=lambda: uuid4().hex)
    user_id: str = Field(default_factory=lambda: uuid4().hex)
    points_amount: float = Field(0.0)
    money_amount: float = Field(0.0)
    last_transaction_id: str | None = Field(None)
    transactions: list[Transaction] = Field(default_factory=list)

    previous_last_transaction_id: str = Field(None)

    def check_last_transaction(self, last_transaction_id_user_knows_about: str) -> bool:
        if last_transaction_id_user_knows_about != self.last_transaction_id:
            raise UserWalletDataIsOutdated("Please refresh wallet details")

    def top_up_balance(self, money_amount: float) -> None:
        transaction = self._create_transaction(money_delta=money_amount, points_delta=0.0, transaction_type=TransactionType.TOP_UP)
        self._notice_transaction(transaction)

    def buy_points(self, point_price: float, points_delta: float) -> None:
        money_delta = -1 * point_price * points_delta
        self._check_is_enough_money(abs(money_delta))
        transaction = self._create_transaction(money_delta=money_delta, points_delta=points_delta, transaction_type=TransactionType.POINTS_ACQUIRING)
        self._notice_transaction(transaction)

    def transfer_to(self, receiver: "Wallet", money_delta: float) -> None:
        money_delta = -1 * money_delta
        self._check_is_enough_money(abs(money_delta))
        transaction = self._create_transaction(money_delta=money_delta, points_delta=0.0, transaction_type=TransactionType.TRANSFER)
        self._notice_transaction(transaction)
        receiver.accept_transfer(transaction)

    def accept_transfer(self, transfer_transaction: Transaction):
        money_delta = -1 * transfer_transaction.money_delta
        incoming_transaction = self._create_transaction(
                money_delta=money_delta,
                points_delta=0.0,
                transaction_type=TransactionType.TRANSFER,
                )
        self._notice_transaction(incoming_transaction)

    def pay_service_fee(self, fee_amount: float):
        money_delta = -1 * fee_amount
        transaction = self._create_transaction(money_delta=money_delta, points_delta=0.0, transaction_type=TransactionType.SERVICE_FEE)
        self._notice_transaction(transaction)


    def _create_transaction(
        self,
        *,
        money_delta: float,
        points_delta: float,
        transaction_type: TransactionType,
    ) -> Transaction:
        return Transaction(
            owner=self.user_id,
            money_delta=money_delta,
            points_delta=points_delta,
            type_=transaction_type,
        )


    def _check_is_enough_money(self, amount_required: float) -> None:
        if amount_required > self.money_amount:
            raise NotEnoughMoneyException(
                f"Not enough money to buy {amount_required} points"
            )

    def _notice_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        self.points_amount += transaction.points_delta
        self.money_amount += transaction.money_delta
        self.previous_last_transaction_id = self.last_transaction_id
        self.last_transaction_id = transaction.id_