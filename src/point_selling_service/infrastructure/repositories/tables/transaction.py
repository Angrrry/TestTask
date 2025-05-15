from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTable

__all__ = ["TransactionTable"]

# previous transaction id uniquity ensures we won't face race conditions during user saving.
# we will catch unique constraint violation if there are already some transaction with previous_transaction, equals this one.


class TransactionTable(BaseTable):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(nullable=False)
    previous_transaction_id: Mapped[str] = mapped_column(
        ForeignKey("transactions.id"),
        nullable=True,
        unique=True,
        sqlite_on_conflict_uniqie="FAIL",
    )
    initiator: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    recipient: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    points_spent: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    money_spent: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
