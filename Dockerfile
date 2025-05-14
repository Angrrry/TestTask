ARG BASE_IMAGE=python:3.10.17-alpine3.21

FROM ${BASE_IMAGE} AS uv-install
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app
RUN python -m pip install uv
COPY ./pyproject.toml ./uv.lock* ./

FROM uv-install AS only-main-dependencies
RUN uv sync --locked --no-install-project --no-dev
COPY --chown=app:app ./src/ /app

FROM only-main-dependencies AS develop
RUN uv sync --locked --no-install-project
CMD ["python", "-m", "point_selling_service", "run"]

FROM ${BASE_IMAGE}

COPY --from=only-main-dependencies --chown=app:app /app /app



CMD ["python", "-m", "point_selling_service", "run"]