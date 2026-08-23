FROM python:3.13-alpine AS migration
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --frozen --group migration

COPY migrations migrations
COPY alembic.ini .

ENTRYPOINT ["uv", "run", "alembic"] 
# ENTRYPOINT cannot be overwritten but you can extend
CMD ["upgrade", "head"] 
# CMD will be completely overwritten (in this case CMD is like a default value)

