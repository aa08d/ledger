from fastapi import FastAPI

from .default import router as default_router
from .healthcheck import router as healthcheck_router
from .ledger import router as ledger_router
from .exceptions import setup_exceptions


def setup_controllers(app: FastAPI) -> None:
    app.include_router(default_router)
    app.include_router(healthcheck_router)
    app.include_router(ledger_router)
    setup_exceptions(app)
