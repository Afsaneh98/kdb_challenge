ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS builder

ENV POETRY_VERSION=2.2.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --only=main --no-root

# second stage: runtime
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder /app/.venv .venv

COPY . .

EXPOSE 8000

CMD ["uvicorn", "kdb_challenge.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]