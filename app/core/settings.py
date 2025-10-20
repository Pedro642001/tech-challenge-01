import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

DOT_ENV = os.path.join(os.path.dirname(__file__), "../../.env")

_model_config = SettingsConfigDict(
    env_file_encoding="utf-8",
    extra="ignore",
)

if os.path.exists(DOT_ENV):
    _model_config["env_file"] = DOT_ENV


class Settings(BaseSettings):
    APP_NAME: str = Field(..., env="APP_NAME")

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    URL_TO_SCRAP: str = Field(..., env="URL_TO_SCRAP")

    API_PREFIX: str = Field(..., env="API_PREFIX")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    ALGORITHM: str = Field("HS256", env="ALGORITHM")

    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(1, env="REFRESH_TOKEN_EXPIRE_DAYS")

    model_config = _model_config


settings = Settings()
