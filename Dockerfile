FROM python:3.10.16-slim-bullseye AS py
RUN python3 -m pip install uv

WORKDIR /app
COPY src src
COPY pyproject.toml uv.lock .python-version ./
RUN uv pip install -r pyproject.toml --system
RUN uv run baml-cli generate --from=src

RUN useradd -u 1001 badrat
USER badrat

WORKDIR /app/src
ENTRYPOINT [ "python3", "-m", "fastapi", "run"]
