from fastapi import FastAPI

from api.routes.router import api_router
from core.config import get_settings


def get_app() -> FastAPI:
    settings = get_settings()

    fast_app = FastAPI(title=settings.app_name, version=settings.app_version)
    fast_app.include_router(api_router, prefix=settings.api_v1_prefix)

    return fast_app


app = get_app()
