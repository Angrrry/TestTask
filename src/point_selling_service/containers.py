from dependency_injector import providers, containers

__all__ = ["Container"]

from point_selling_service.application.wallet_service import WalletService
from point_selling_service.domain.model import IQueryWalletRepository, ICommandWalletRepository, IUserRepository
from point_selling_service.infrastructure.repositories import CommandWalletRepository, UserRepository


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()

    wallet: providers.Singleton[ICommandWalletRepository] = providers.Singleton(CommandWalletRepository,connection_string=config.database.connection_string)
    user: providers.Singleton[IUserRepository] = providers.Singleton(UserRepository, connection_string=config.database.connection_string)

class Applications(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories = providers.DependenciesContainer()

    wallet: providers.Singleton[WalletService] = providers.Singleton(WalletService,user_repository=repositories.user, command_wallet_repository=repositories.wallet)

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    repositories: providers.Container[Repositories] = providers.Container(Repositories,config=config)
    applications: providers.Container[Applications] = providers.Container(Applications, config=config, repositories=repositories)