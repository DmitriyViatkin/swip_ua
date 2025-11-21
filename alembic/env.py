import os
import sys
from logging.config import fileConfig

# --------------------------------------------------------------------
# 1. Добавляем путь к проекту
# --------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --------------------------------------------------------------------
# 2. Alembic + настройки
# --------------------------------------------------------------------
from alembic import context
config = context.config
fileConfig(config.config_file_name)

# --------------------------------------------------------------------
# 3. Настройки проекта
# --------------------------------------------------------------------
from core.infra.config.settings import get_infra_settings
settings = get_infra_settings()

# --------------------------------------------------------------------
# 4. Sync URL для Alembic (async → sync)
# --------------------------------------------------------------------
db_url = str(settings.db.url)

if db_url.startswith("postgresql+asyncpg"):
    sync_url = db_url.replace("postgresql+asyncpg", "postgresql")
elif db_url.startswith("sqlite+aiosqlite"):
    sync_url = db_url.replace("sqlite+aiosqlite", "sqlite")
else:
    sync_url = db_url

print(f"[DEBUG] Sync DB URL = {sync_url}")

config.set_main_option("sqlalchemy.url", sync_url)

# --------------------------------------------------------------------
# 5. Импортируем Base и МОДЕЛИ — очень важно делать до target_metadata
# --------------------------------------------------------------------
from src.database import Base
import src.users.models
import src.building.models
import src.listings.models

# --------------------------------------------------------------------
# 6. Передаем meta Alembic
# --------------------------------------------------------------------
target_metadata = Base.metadata

# DEBUG: проверить, что Alembic видит таблицы
print("=== TABLES LOADED ===")
print(Base.metadata.tables.keys())

# --------------------------------------------------------------------
# 7. OFFLINE MODE
# --------------------------------------------------------------------
def run_migrations_offline():
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# --------------------------------------------------------------------
# 8. ONLINE MODE
# --------------------------------------------------------------------
from sqlalchemy import create_engine, pool

def run_migrations_online():
    engine = create_engine(sync_url, poolclass=pool.NullPool)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# --------------------------------------------------------------------
# 9. RUN
# --------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
