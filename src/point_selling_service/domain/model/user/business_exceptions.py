__all__ = [
    "BasePointSellingException",
    "NotEnoughMoneyException",
    "UserNotFountException",
]


class BasePointSellingException(Exception): ...


class NotEnoughMoneyException(BasePointSellingException): ...


class UserNotFountException(BasePointSellingException): ...


class TransactionCannotBeSaved(BasePointSellingException): ...
