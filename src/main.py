import logging

from fastapi import FastAPI

from api.routes.router import api_router
from core.config import get_settings
from core.event_handlers import lifespan


def get_app() -> FastAPI:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()

    fast_app = FastAPI(
        title=settings.app_name, version=settings.app_version, lifespan=lifespan
    )
    fast_app.include_router(api_router, prefix=settings.api_prefix)

    return fast_app


app = get_app()
