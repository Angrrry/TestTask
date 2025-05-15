__all__ = [
    "BasePointSellingException",
    "NotEnoughMoneyException",
    "UserNotFoundException",
    "UserWalletDataIsOutdated",
        "WalletIsOutdated",

]

class BasePointSellingException(Exception): ...

class NotEnoughMoneyException(BasePointSellingException): ...

class UserNotFoundException(BasePointSellingException): ...

class TransactionCannotBeSaved(BasePointSellingException): ...

class UserWalletDataIsOutdated(BasePointSellingException): ...

class WalletIsOutdated(BasePointSellingException): ...