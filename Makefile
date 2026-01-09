.PHONY: api celery dev

# Запуск FastAPI
api:
	poetry run uvicorn config.app:app --reload

# Запуск Celery worker
celery:
	poetry run celery -A config.infra.utils.celery_app.celery_app worker --loglevel=info


# Применить миграции
migrate:
	poetry run alembic upgrade head

# Создать новую миграцию (использование: make revision m="сообщение")
revision:
	poetry run alembic revision --autogenerate -m "$(m)" # make revision m=" Description migration"

# Одновременный запуск (2 терминала)
dev:
	@echo "Run API and Celery in separate terminals"
	@echo "make api"
	@echo "make celery"

