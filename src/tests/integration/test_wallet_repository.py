from point_selling_service.domain.model import ICommandWalletRepository, Wallet
from point_selling_service.infrastructure.repositories import CommandWalletRepository
import pytest

@pytest.fixture
def test_wallet():
    return Wallet(last_transaction_id=None)


def test_save_wallet_get_wallet__correct_wallet(wallet_command_repository: ICommandWalletRepository, test_wallet: Wallet):
    wallet_command_repository.save_wallet(test_wallet)
    assert wallet_command_repository.get_wallet(test_wallet.user_id) == test_wallet

def test_update_wallet__with_transaction__wallet_is_updated(wallet_command_repository: ICommandWalletRepository, test_wallet: Wallet):
    wallet_command_repository.save_wallet(test_wallet)
    test_wallet.top_up_balance(5.0)
    wallet_command_repository.save_wallet(test_wallet)
    test_wallet.transactions.clear()
    wallet_from_db = wallet_command_repository.get_wallet(test_wallet.user_id)
    assert test_wallet == wallet_from_db

