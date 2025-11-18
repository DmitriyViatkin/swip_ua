""" Settings configuration for the User service application. """

from functools import lru_cache
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.infra.config.settings import (BaseInfraSettings, InfraSettings,
                                      get_infra_settings)


class UserSettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="USER_SERVICE_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    TITLE: str = "User Service"
    DESCRIPTION: str = "FastAPI app for User Service"


    infra: InfraSettings = Field(default_factory=get_infra_settings)


@lru_cache
def get_settings() -> UserSettings:
    return UserSettings()


user_settings: UserSettings = get_settings()
