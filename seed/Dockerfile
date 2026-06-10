FROM python:3.12-alpine3.22

COPY --from=ghcr.io/astral-sh/uv:0.10.5 /uv /uvx /bin/

WORKDIR /app

COPY seed/requirements.txt .
COPY seed/uv.lock .
COPY seed/pyproject.toml .

# Install system dependencies required for building Python packages
RUN apk update && apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    openssl-dev \
    libstdc++

# Sync dependencies
RUN uv sync --frozen --no-dev

# Copy the src directory and seed.py
COPY seed/src ./src
COPY seed/seed.py .

# Set PYTHONPATH to include /app
ENV PYTHONPATH=/app

CMD ["uv", "run", "python", "seed.py"]
