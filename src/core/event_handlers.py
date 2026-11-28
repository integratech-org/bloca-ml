import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import get_settings
from services.utils import HFFileDownloader, JoblibModelLoader, TFLiteModelLoader

logger = logging.getLogger(__name__)


def _startup_models(app: FastAPI) -> None:
    settings = get_settings()
    downloader = HFFileDownloader(
        repo_id=settings.hf_repo_id,
        repo_revision=settings.hf_repo_revision,
        model_directory=settings.models_directory,
    )

    app.state.strength_model = None
    app.state.surface_model = None

    try:
        app.state.strength_model = JoblibModelLoader(
            downloader=downloader, filename=settings.strength_filename
        ).load()
    except Exception as exc:
        logger.error(f"Failed to load strength model: {exc}")
        raise RuntimeError(f"Failed to load strength model: {exc}") from exc

    try:
        app.state.surface_model = TFLiteModelLoader(
            downloader=downloader, filename=settings.surface_filename
        ).load()
    except Exception as exc:
        logger.error(f"Failed to load surface model: {exc}")
        raise RuntimeError(f"Failed to load surface model: {exc}") from exc


def _shutdown_models(app: FastAPI) -> None:
    app.state.strength_model = None
    app.state.surface_model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running app startup handler.")
    _startup_models(app)
    yield
    logger.info("Running app shutdown handler.")
    _shutdown_models(app)
