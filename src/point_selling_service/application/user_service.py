import logging

from point_selling_service.domain.model import User, UserNotFoundException, IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user(self, id_: str) -> User | None:
        if not self._user_repository.get_user(id_):
            raise UserNotFoundException(f"User with id {id_} not found")

    def top_up_balance(self, id_: str, amount: float) -> None:
        user = self.get_user(id_)
        user.top_up_balance(amount)
        self._user_repository.save_user(user)

    def transfer_money(self, id_: str, receiver_id: str, amount: float) -> None:
        current_user = self.get_user(id_)
        receiver_user = self.get_user(receiver_id)
        current_user.transfer_to(receiver=receiver_user, money_amount=amount)
        self._user_repository.save_user(current_user)