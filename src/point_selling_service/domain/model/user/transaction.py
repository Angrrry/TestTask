from datetime import datetime, timezone
from typing import Any
from enum import Enum
from uuid import uuid4
from pydantic import BaseModel, model_validator, Field

__all__ = ["Transaction", "SYSTEM_IDENTITY_ID"]

SYSTEM_IDENTITY_ID = "SYSTEM"


class TransactionType(Enum):
    TRANSFER = "Transfer"
    POINTS_ACQUIRING = "Points Acquiring"
    TOP_UP = "Top Up"
    SERVICE_FEE = "Service Fee"


class Transaction(BaseModel):
    # I'm not a fan of pydantic in domain models, using it here in sake of data validation
    id_: str = Field(default_factory=lambda: uuid4().hex)
    from_: str
    to: str = Field(SYSTEM_IDENTITY_ID)
    transaction_type: TransactionType
    points_delta: float = Field(0.0)
    money_delta: float = Field(0.0)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def _validate_has_changes(self):
        if not self.points_delta and not self.money_delta:
            raise ValueError("Transaction must have at least one change")
        return self

    def __eq__(self, other: Any):
        return isinstance(other, self.__class__) and self.id_ == other.id_
