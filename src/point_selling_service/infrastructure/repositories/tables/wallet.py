from .base import BaseTable
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

__all__ = ["WalletTable"]


class WalletTable(BaseTable):
    __tablename__ = "wallets"
    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    points_amount: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    money_amount: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    last_transaction_id: Mapped[str] = mapped_column(ForeignKey("transactions.id"), nullable=True)

