FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry
RUN poetry config virtualenvs.create false
RUN poetry self add poetry-plugin-export

# Копируем зависимости **относительно корня проекта**
COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

COPY . .