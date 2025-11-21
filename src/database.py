from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from core.infra.config.settings import get_infra_settings
from typing import AsyncGenerator

Base = declarative_base()  # <- только Base

settings = get_infra_settings()
database_settings = settings.db

def get_async_engine():
    return create_async_engine(database_settings.url, echo=database_settings.ECHO)

AsyncSessionLocal = async_sessionmaker(
    bind=get_async_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    # Импортируем все модели здесь
    import src.users.models
    import src.building.models
    import src.advert.models

    engine = get_async_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
