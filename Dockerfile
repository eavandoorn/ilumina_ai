FROM python:3.12-slim as base

ENV PY_VERSION=3.12
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    graphicsmagick \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src/requirements.txt .
RUN uv pip install --system -r requirements.txt

COPY src/ .

# Development server for the sandbox environment
EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]


