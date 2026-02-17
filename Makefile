.PHONY: api celery migrate revision test \
        docker-build docker-up docker-down docker-restart \
        docker-logs docker-clean docker-migrate docker-revision start

# Переменные для удобства
COMPOSE_PATH = -f deploy/docker-compose.yml
COMPOSE = docker compose $(COMPOSE_PATH)

# ================= LOCAL / INSIDE CONTAINER =================
# Эти команды запускаются либо локально, либо используются как ENTRYPOINT в Docker

# Полный цикл запуска приложения (используется в Docker командой CMD/ENTRYPOINT)
start:
	poetry run alembic upgrade head
	poetry run uvicorn config.app:app --host 0.0.0.0 --port 8000

# Запуск только API
api:
	poetry run uvicorn config.app:app --reload

# Запуск Celery worker
celery:
	poetry run celery -A config.infra.utils.celery_app.celery_app worker --loglevel=info

# Применить миграции (внутри текущего окружения)
migrate:
	poetry run alembic upgrade head

# Создать новую миграцию (нужно передать m="описание")
revision:
	poetry run alembic revision --autogenerate -m "$(m)"

# Тесты
test:
	poetry run pytest

# ================= DOCKER (EXTERNAL CONTROL) =================
# Эти команды запускай со своего основного терминала (dima@dima-...)

# Собрать образы
docker-build:
	$(COMPOSE) build

# Запустить проект в фоне
docker-up:
	$(COMPOSE) up -d

# Остановить проект
docker-down:
	$(COMPOSE) down

# Перезапуск с пересборкой
docker-restart:
	$(COMPOSE) down && $(COMPOSE) up -d --build

# Логи всех контейнеров
docker-logs:
	$(COMPOSE) logs -f

# Полная очистка: удалить контейнеры, сети и ТОМА (базу данных)
docker-clean:
	$(COMPOSE) down -v --remove-orphans

# Применить миграции ВНУТРИ запущенного контейнера web
docker-migrate:
	$(COMPOSE) run --rm web poetry run alembic upgrade head

# Создать миграцию ЧЕРЕЗ контейнер (используй: make docker-revision m="migration_name")
docker-revision:
	$(COMPOSE) run --rm web poetry run alembic revision --autogenerate -m "$(m)"