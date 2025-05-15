from ..tables import TransactionTable, WalletTable
from point_selling_service.domain.model import Transaction, Wallet

__all__ = ["WalletMapper", "TransactionMapper"]

class TransactionMapper:
    @classmethod
    def from_domain(cls, transaction: Transaction) -> TransactionTable:
        return TransactionTable(
                id=transaction.id_,
                owner=transaction.owner,
                type=transaction.type_.value,
                points_delta=transaction.points_delta,
                money_delta=transaction.money_delta,
                timestamp=transaction.timestamp,
                )

class WalletMapper:
    @classmethod
    def from_command_table_response(cls, response: WalletTable):
        return Wallet(
                id_=response.id,
        user_id=response.user_id,
        points_amount=response.points_amount,
        money_amount=response.money_amount,
        last_transaction_id=response.last_transaction_id,
        transactions=[]
                )
    @classmethod
    def from_domain(cls, wallet: Wallet) -> tuple[WalletTable, list[TransactionTable]]:
        return (
            WalletTable(
                id=wallet.id_,
                user_id=wallet.user_id,
                points_amount=wallet.points_amount,
                money_amount=wallet.money_amount,
                last_transaction_id=wallet.last_transaction_id,
                ), [*map(TransactionMapper.from_domain, wallet.transactions)]
            )
