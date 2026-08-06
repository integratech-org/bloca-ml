from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "bloca-ml"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"

    api_key: str
    is_debug: bool = True


@lru_cache
def get_settings():
    return Settings()  # type: ignore
