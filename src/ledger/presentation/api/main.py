import logging
import uvicorn

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from ledger.presentation.api.controllers import setup_controllers

from .config import APIConfig


logger = logging.getLogger(__name__)


def init_api(container: AsyncContainer, debug: bool = __debug__,) -> FastAPI:
    logger.info(f"Initializing API")

    app = FastAPI(
        debug=debug,
        title="Ledger API",
        version="1.0.0",
    )

    setup_controllers(app)
    setup_dishka(container, app)

    return app


async def run_api(app: FastAPI, config: APIConfig) -> None:
    config = uvicorn.Config(
        app=app,
        host=config.host,
        port=config.port,
        log_level=logging.INFO,
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info(f"Running server on {config.host}:{config.port}")
    await server.serve()
