from point_selling_service.domain.model import ICommandWalletRepository, Wallet, WalletIsOutdated
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from .query_factory import CommandWalletQueryFactory
from .mappers import WalletMapper

__all__ = ["CommandWalletRepository"]

class CommandWalletRepository(ICommandWalletRepository):
    def __init__(self, connection_string: str):
        self._engine = create_engine(connection_string)

    def get_wallet(self, user_id: str) -> Wallet | None:
        with Session(self._engine) as session:
            wallet_table = session.execute(CommandWalletQueryFactory.select_wallet(user_id)).scalar_one_or_none()
        return wallet_table and WalletMapper.from_command_table_response(wallet_table)

    def save_wallet(self, wallet: Wallet) -> None:
        with Session(self._engine) as session:
            self._do_save_iside_transaction(session, wallet)
            session.commit()

    def save_wallets(self, *wallets: Wallet) -> None:
        with Session(self._engine) as session:
            for wallet in wallets:
                self._do_save_iside_transaction(session, wallet)
            session.commit()

    def _do_save_iside_transaction(self, session, wallet):
        db_wallet = session.execute(CommandWalletQueryFactory.select_wallet(wallet.user_id)).scalar_one_or_none()
        if db_wallet and db_wallet.last_transaction_id != wallet.previous_last_transaction_id:
            raise WalletIsOutdated("Somebody commited something before us, need to refresh wallet.")
        wallet_table, transactions = WalletMapper.from_domain(wallet)
        session.merge(wallet_table)
        session.add_all(transactions)