FROM ghcr.io/astral-sh/uv:python3.13-alpine
WORKDIR /app
COPY src src
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync
RUN uv run baml-cli generate --from=src

RUN adduser -S -u 1001 -D badrat
USER badrat

WORKDIR /app/src
ENTRYPOINT [ "uv", "run", "fastapi", "run"]
