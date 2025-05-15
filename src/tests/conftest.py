import pytest

from point_selling_service.entrypoint import create_fastapi, init_container
from point_selling_service.settings import Settings


# from fastapi.testclient import TestClient

@pytest.fixture(scope="session")
def app():
    settings = Settings()
    container = init_container(settings)
    fastapi_app = create_fastapi(container)
    yield fastapi_app



# @pytest.fixture
# def client(app):
#     with TestClient(app) as client:
#         yield client


@pytest.fixture(scope="session")
def session_containers(app):
    return app.container


@pytest.fixture
def containers(session_containers):
    with session_containers.reset_singletons():
        yield session_containers

