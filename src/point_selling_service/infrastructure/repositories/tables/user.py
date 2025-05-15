from sqlalchemy.orm import Mapped, mapped_column, relationship

from .transaction import TransactionTable
from .base import BaseTable
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, desc, func

__all__ = ["UserTable"]


class UserTable(BaseTable):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
