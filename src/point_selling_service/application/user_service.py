import datetime
import logging
from typing import Protocol

from point_selling_service.domain.model import User, UserNotFoundException


class UserService:
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository
        self._logger = logging.getLogger(self.__class__.__name__)

    def get_user(self, id_: str) -> User | None:
        return self._user_repository.get_user(id_)
