from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "bloca-ml"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"

    api_key: str
    is_debug: bool = True

    models_directory: Path = Path("./ml_models")

    hf_repo_id: str
    hf_repo_revision: str = "main"

    strength_filename: str = "strength_rf.joblib"
    surface_filename: str = "surface_defect_mobilenetv2.tflite"


@lru_cache
def get_settings():
    return Settings()  # type: ignore
