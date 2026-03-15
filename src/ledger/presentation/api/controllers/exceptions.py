import logging
from functools import partial
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from ledger.domain.common.exceptions import AppException
from ledger.application.ledger.exceptions import LedgerNotFoundException, TransactionNotFoundException
from ledger.domain.ledger.exceptions import LedgerCannotTransition
from ledger.presentation.api.controllers.responses.base import ExceptionData, ExceptionResponse


logger = logging.getLogger(__name__)


def setup_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(AppException, error_handler(500))
    app.add_exception_handler(LedgerNotFoundException, status.HTTP_404_NOT_FOUND)
    app.add_exception_handler(TransactionNotFoundException, status.HTTP_404_NOT_FOUND)
    app.add_exception_handler(LedgerCannotTransition, status.HTTP_400_BAD_REQUEST)
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[JSONResponse]]:
    return partial(app_exception_handler, status_code=status_code)


async def app_exception_handler(
    request: Request,
    exception: AppException,
    status_code: int,
) -> JSONResponse:
    return await handle_exception(
        request=request,
        exception=exception,
        exception_data=ExceptionData(message=exception.message, data=exception),
        status=exception.status,
        status_code=status_code,
    )


async def unknown_exception_handler(request: Request, exception: Exception) -> JSONResponse:
    logger.error("Handle error", exc_info=exception, extra={"exception": exception})
    logger.exception("Unknown error occurred", exc_info=exception, extra={"exception": exception})
    return JSONResponse(
        ExceptionResponse(exception=ExceptionData(data=exception)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_exception(
    request: Request,
    exception: Exception,
    exception_data: ExceptionData,
    status: int,
    status_code: int,
) -> JSONResponse:
    logger.exception("Handle exception", exc_info=exception, extra={"exception": exception})
    return JSONResponse(
        ExceptionResponse(exception=exception_data, status=status),
        status_code=status_code,
    )
