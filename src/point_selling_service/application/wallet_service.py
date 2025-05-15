from point_selling_service.domain.model import IUserRepository, ICommandWalletRepository, Wallet, UserNotFoundException

__all__ = ["WalletService"]

class WalletService:
    def __init__(self, user_repository: IUserRepository, command_wallet_repository: ICommandWalletRepository):
        self._user_repository = user_repository
        self._command_wallet_repository = command_wallet_repository
        self._point_price: float = 1.

    def get_wallet(self, user_id: str) -> Wallet | None:
        if wallet:= self._command_wallet_repository.get_wallet(user_id):
            return wallet
        raise UserNotFoundException(f"User with id {user_id} not found")

    def top_up_wallet(self, client_side_last_transaction_id: str | None, user_id: str, top_up_amount: float) -> Wallet:
        wallet = self.get_wallet(user_id)
        wallet.check_last_transaction(client_side_last_transaction_id)
        wallet.top_up_balance(top_up_amount)
        self._command_wallet_repository.save_wallet(wallet)
        return wallet

    def buy_points(self, client_side_last_transaction_id: str | None, user_id: str, amount: float):
        wallet = self.get_wallet(user_id)
        wallet.check_last_transaction(client_side_last_transaction_id)
        wallet.buy_points(points_delta=amount, point_price=self._point_price)
        self._command_wallet_repository.save_wallet(wallet)
        return wallet

    def transfer_to(self, user_id: str, receiver_id: str, amount: float, client_side_last_transaction_id: str | None):
        # Probably modifying 2 objects at the same time is against the rules, but I just don't have time, sorry.
        # same for batch querying of wallets

        wallet = self.get_wallet(user_id)
        receiver_wallet = self.get_wallet(receiver_id)
        wallet.check_last_transaction(client_side_last_transaction_id)
        wallet.transfer_to(receiver_wallet, amount)
        self._command_wallet_repository.save_wallets(wallet, receiver_wallet)

    # TODO: Process Service fee
    