from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseTable

__all__ = ["TransactionTable"]

class TransactionTable(BaseTable):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True)
    owner: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    points_delta: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    money_delta: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
