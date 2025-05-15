import pytest
from point_selling_service.infrastructure.repositories.tables.base import BaseTable
from sqlalchemy import create_engine

@pytest.fixture
def connection_engine(containers):
    connection_string = containers.config.database.connection_string()
    engine = create_engine(connection_string, echo=True)
    return engine

@pytest.fixture(autouse=True)
def init_database(connection_engine):
    BaseTable.metadata.create_all(connection_engine)

@pytest.fixture
def repositories(containers):
    return containers.repositories

@pytest.fixture
def wallet_command_repository(repositories, connection_engine):
    repo =  repositories.wallet()
    repo._engine = connection_engine
    return repo

@pytest.fixture
def user_repository(repositories, connection_engine):
    repo = repositories.user()
    repo._engine = connection_engine
    return repo

@pytest.fixture
def wallet_application(containers, user_repository, wallet_command_repository):
    return containers.applications.wallet()
