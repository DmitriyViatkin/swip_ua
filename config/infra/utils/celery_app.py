import os
import sys

from celery import Celery
from config.infra.config.settings import infra_settings

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(0, BASE_DIR)

celery_app = Celery(
    "tasks",
    broker=infra_settings.celery.BROKER_URL,
    backend=infra_settings.celery.RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer=infra_settings.celery.TASK_SERIALIZER,
    result_serializer=infra_settings.celery.RESULT_SERIALIZER,
    accept_content=infra_settings.celery.ACCEPT_CONTENT,
    timezone=infra_settings.celery.TIMEZONE,
    enable_utc=infra_settings.celery.ENABLE_UTC,
    broker_connection_retry_on_startup=True,
)

celery_app.autodiscover_tasks(["src.auth.tasks.py"])