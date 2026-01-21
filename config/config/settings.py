""" Settings configuration for the User service application. """

from functools import lru_cache
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.infra.config.settings import (BaseInfraSettings, InfraSettings,
                                      get_infra_settings)


class UserSettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="USER_SERVICE_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    TITLE: str = "Swipe"
    DESCRIPTION: str = "FastAPI app for Swipe"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    BASE_URL: str = Field(default="http://localhost:8000")
    MEDIA_PREFIX: str = "/media/"

    @property
    def media_url(self) -> str:
        
        return f"{self.BASE_URL.rstrip('/')}{self.MEDIA_PREFIX}"

    infra: InfraSettings = Field(default_factory=get_infra_settings)



@lru_cache
def get_settings() -> UserSettings:
    return UserSettings()


user_settings: UserSettings = get_settings()
