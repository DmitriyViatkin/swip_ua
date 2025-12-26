.PHONY: api celery dev

# Запуск FastAPI
api:
	poetry run uvicorn config.app:app --reload

# Запуск Celery worker
celery:
	poetry run celery -A config.infra.utils.celery_app.celery_app worker --loglevel=info

# Одновременный запуск (2 терминала)
dev:
	@echo "Run API and Celery in separate terminals"
	@echo "make api"
	@echo "make celery"

