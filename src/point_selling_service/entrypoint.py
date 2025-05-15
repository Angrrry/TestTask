from fastapi import FastAPI
from .containers import Container
from .constants import *
from .settings import Settings
import uvicorn


def init_container(settings):
    container = Container()
    container.config.from_pydantic(settings)
    container.init_resources()
    # container.wire(
    #         ...
    #         )
    return container


def create_fastapi(container: Container):
    fastapi_app = FastAPI(
        title=PROJECT_NAME,
        docs_url=DOCUMENTATION_URL
        if container.config.documentation_enabled()
        else None,
    )
    ...
    fastapi_app.container = container
    return fastapi_app


def run_api():
    settings = Settings()
    container = init_container(settings)
    fastapi_app = create_fastapi(container)
    uvicorn.run(fastapi_app)
