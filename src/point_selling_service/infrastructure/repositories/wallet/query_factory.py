from sqlalchemy import select

from ..tables import WalletTable

__all__ = ["CommandWalletQueryFactory"]

class CommandWalletQueryFactory:
    @classmethod
    def select_wallet(cls, user_id: str) -> select:
        return select(WalletTable).where(WalletTable.user_id == user_id)
