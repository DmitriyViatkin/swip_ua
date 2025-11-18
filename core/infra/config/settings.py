from typing import Any, ClassVar, Optional
from pathlib import Path
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

# --- BASE CLASS ---

class BaseInfraSettings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent.parent)


# --- REDIS SETTINGS ---

class RedisSettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="REDIS_"
    )

    HOST: str = "localhost"
    PORT: int = 6377
    PASSWORD: Optional[str] = None
    DB: int = 0

    @property
    def url(self) -> str:
        if self.PASSWORD:
            return f"redis://:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


# --- DATABASE SETTINGS ---

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from sqlalchemy import event


class DatabaseSettings(BaseInfraSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="DB_"
    )

    HOST: str = "localhost"
    PORT: int = 5432
    USER: Optional[str] = None
    PASSWORD: Optional[str] = None
    DB: Optional[str] = None

    ECHO: bool = False
    ECHO_POOL: bool = False
    POOL_DISABLED: bool = False
    POOL_MAX_OVERFLOW: Optional[int] = None
    POOL_SIZE: int = 5
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 3600
    POOL_PRE_PING: bool = False

    _engine_instance: Optional[AsyncEngine] = None

    @property
    def url(self) -> str:
        if all([self.USER, self.PASSWORD, self.DB]):
            return (
                f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@"
                f"{self.HOST}:{self.PORT}/{self.DB}"
            )
        return "sqlite+aiosqlite:///db.sqlite3"

    def _build_engine_params(self) -> dict[str, Any]:
        params = {
            "url": self.url,
            "future": True,
            "echo": self.ECHO,
            "echo_pool": self.ECHO_POOL,
            "pool_recycle": self.POOL_RECYCLE,
            "pool_pre_ping": self.POOL_PRE_PING,
        }

        if not self.url.startswith("sqlite"):
            params.update(
                pool_size=self.POOL_SIZE,
                pool_timeout=self.POOL_TIMEOUT,
                pool_use_lifo=True,
            )

            if self.POOL_MAX_OVERFLOW is not None:
                params["max_overflow"] = self.POOL_MAX_OVERFLOW

            if self.POOL_DISABLED:
                params["poolclass"] = NullPool

        return params

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance:
            return self._engine_instance

        params = self._build_engine_params()
        engine = create_async_engine(**params)

        if self.url.startswith("sqlite"):
            @event.listens_for(engine.sync_engine, "connect")
            def _connect(dbapi_connection, connection_record):
                dbapi_connection.isolation_level = None

            @event.listens_for(engine.sync_engine, "begin")
            def _begin(dbapi_connection):
                dbapi_connection.exec_driver_sql("BEGIN")

        self._engine_instance = engine
        return engine


# --- MAIN CONTAINER ---

class InfraSettings(BaseInfraSettings):
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)


# ❗ правильная единственная функция получения настроек
@lru_cache
def get_settings() -> InfraSettings:
    return InfraSettings()

@lru_cache
def get_infra_settings() -> InfraSettings:
    return InfraSettings()

infra_settings = get_infra_settings()
# экспортируем готовый объект
infra_settings = get_settings()

database_settings = infra_settings.db
redis_settings = infra_settings.redis
